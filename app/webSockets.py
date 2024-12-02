# app/posts_path.py
from flask import Blueprint, request, jsonify, current_app, render_template
from flask_sock import Sock
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import html
import asyncio

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
    client_address = ws.environ.get('REMOTE_ADDR')
    print(f"WebSocket connection established from {client_address}")
    try:
        while True:
            # Wait for incoming messages
            data = ws.receive()
            if data:
                print(f"Received message from {client_address}")
                sanitized_data = html.escape(data)
                conn = get_db_connection()
                cursor = conn.cursor()
                insert_query = """
                INSERT INTO messages (sender, content)
                VALUES (%s, %s)
                RETURNING id;
                """
                cursor.execute(insert_query, (client_address, sanitized_data))
                message_id = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                conn.close()

                print(f"Message stored with ID: {message_id}")

                # Broadcast the message to all connected clients
                asyncio.ensure_future(broadcast_message(f"{client_address}: {sanitized_data}"))

    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        # Unregister the client on disconnect
        WEBSOCKET_CONNECTIONS.remove(ws)
        print(f"WebSocket connection closed for {client_address}")

async def broadcast_message(message):
    """Broadcasts a message to all connected WebSocket clients."""
    if WEBSOCKET_CONNECTIONS:
        await asyncio.wait([client.send(message) for client in WEBSOCKET_CONNECTIONS])
