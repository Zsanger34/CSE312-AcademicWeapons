# app/posts_path.py
from flask import Blueprint, request, jsonify, current_app, render_template
from flask_sock import Sock
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import json
from datetime import datetime
import time


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
                data = json.loads(data)
                scheduled_time = data.get('scheduled_time')
                data = data.get('message_content')
                if scheduled_time is None:
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
                        "created_at": time_ago(post[4]) ,#post[4].strftime('%Y-%m-%d %H:%M:%S'),
                        "profile_id": post[5],
                        "profile_picture_url": post[6]
                    }

                    broadcast_message(format_post)
                    
                else:
                    schedulePost(scheduled_time, data, user)

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


def time_ago(post_time):
    
    now = datetime.now()
    diff = now - post_time
    print(diff, flush=True)
    if diff.days > 1:
        return f"{diff.days} days ago"
    elif diff.days == 1:
        return "1 day ago"
    elif diff.seconds >= 3600:
        return f"{diff.seconds // 3600} hours ago"
    elif diff.seconds >= 60:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return "just now"




def schedulePost(timeScheduled, post, user):
    timeScheduled = datetime.fromisoformat(timeScheduled)
    print("scheduling Posts", flush=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO schedulePosts (post_schedule_time, post_data, username) VALUES (%s, %s, %s)", (timeScheduled, post, user))

    conn.commit()
    cursor.close()
    conn.close()



def handleSchedulePosts():
    while True:
        currentTime = datetime.now()
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM schedulePosts WHERE post_schedule_time <= %s"
        cursor.execute(query, (currentTime,))

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if results:
            print("scheudled Post found", flush=True)
            conn = get_db_connection()
            cursor = conn.cursor()
            for post in results:
                print(post)
                postID = post[0]
                postTime = post[1]
                postData = post[2]
                username = post[3]
                cursor.execute("DELETE FROM schedulePosts WHERE post_id = %s", (postID,))
                cursor.execute("""
                    INSERT INTO messages (user_id, message_content) 
                    VALUES (%s, %s) RETURNING message_id
                """, (username, postData))
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
                    "created_at": time_ago(post[4]) ,#post[4].strftime('%Y-%m-%d %H:%M:%S'),
                    "profile_id": post[5],
                    "profile_picture_url": post[6]
                }

                broadcast_message(format_post)
        
        time.sleep(50)
        