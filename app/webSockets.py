# app/posts_path.py
from flask import Blueprint, request, jsonify, current_app, render_template
from flask_sock import Sock
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import json

# Initialize Sock
sock = Sock()

# Set to keep track of connected WebSocket clients
WEBSOCKET_CONNECTIONS = set()

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        host='db',  # Replace with your DB host
        database='mydatabase',  # Replace with your DB name
        user='postgres',  # Replace with your DB user
        password='mysecretpassword'  # Replace with your DB password
    )
    return conn

@sock.route('/establish_POSTS_Connection')
def websocket_connection(ws):
    """Handles WebSocket connections for the /establish_POSTS_Connection route."""
    WEBSOCKET_CONNECTIONS.add(ws)

    conn = get_db_connection()
    cursor = conn.cursor()
    #lets make a new user_id
    session_token = request.cookies.get('session_token')
    hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
    cursor.execute('SELECT id FROM users WHERE cookie = %s', (hashed_token,))
    user = cursor.fetchone()[0]
    cursor.close()
    conn.close()


    client_address = ws.environ.get('REMOTE_ADDR')
    print(f"WebSocket connection established from {client_address}", flush=True)
    try:
        while True:
            # Wait for incoming messages
            data = ws.receive()
            if data:
                print(data, flush=True)
                data = json.loads(data)
                data = data.get('message_content')
                print(f"Received message from {client_address}")

                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO messages (user_id, message_content) 
                    VALUES (%s, %s) RETURNING message_id
                """, (user, data))
                message_id = cursor.fetchone()[0]
                conn.commit()

                cursor.execute("""
                    SELECT messages.message_id, 
                        users.username, 
                        messages.message_content, 
                        messages.likes, 
                        messages.created_at, 
                        profilePages.profile_id, 
                        profilePages.profilePictureUrl
                    FROM messages
                    JOIN users ON messages.user_id = users.id
                    JOIN profilePages ON users.profile_id = profilePages.profile_id
                    WHERE messages.message_id = %s;
                """, (message_id,))
                post = cursor.fetchone()

                cursor.close()
                conn.close()

                print(f"Message stored with ID: {message_id}", flush=True)

                # Broadcast the message to all connected clients
                format_post = {
                    "message_id": post[0],
                    "username": post[1],
                    "message_content": post[2],
                    "likes": post[3],
                    "created_at": post[4].strftime('%Y-%m-%d %H:%M:%S'),
                    "profile_id": post[5],
                    "profile_picture_url": post[6]
                }
                broadcast_message(format_post)

    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        # Unregister the client on disconnect
        WEBSOCKET_CONNECTIONS.remove(ws)
        print(f"WebSocket connection closed for {client_address}")

def broadcast_message(message):
    """Broadcasts a message to all connected WebSocket clients."""
    message = json.dumps(message)
    for client in WEBSOCKET_CONNECTIONS:
        try:
            client.send(message)
        except Exception as e:
            print(f"Failed to send message to client: {e}")
            WEBSOCKET_CONNECTIONS.remove(client)

