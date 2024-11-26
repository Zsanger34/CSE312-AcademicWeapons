# app/posts_path.py
from flask import Blueprint, request, jsonify, current_app
from flask_sock import Sock
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import html

def get_db_connection():
    conn = psycopg2.connect(
        host='db', database='mydatabase', user='postgres', password='mysecretpassword'
    )
    return conn

# Initialize Sock in the blueprint
sock = Sock()
WEBSOCKETCONNECTIONS = set()


@sock.route('/establish_POSTS_Connection')
def websocket_connection(ws):
    # Establishing WebSocket connection
    WEBSOCKETCONNECTIONS.add(ws)
    print("WebSocket connection established")
    while True:
        # Receive data from the WebSocket
        data = ws.receive()
        if data:
            print(f"Received message: {data}")