# app/posts_path.py

from flask import Blueprint, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib

# Blueprint setup for modularity
posts_bp = Blueprint('posts', __name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='db', database='mydatabase', user='postgres', password='mysecretpassword'
    )
    return conn

@posts_bp.route('/messages', methods=['POST'])
def create_message():
    """Submit a new message and store it in the messages table"""
    data = request.get_json()
    user_id = data.get('user_id')
    message_content = data.get('message_content')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    #lets make a new user_id
    session_token = request.cookies.get('session_token')
    hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
    cursor.execute('SELECT id FROM users WHERE cookie = %s', (hashed_token,))
    user = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO messages (user_id, message_content) 
        VALUES (%s, %s) RETURNING message_id
    """, (user, message_content))
    message_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message_id': message_id, 'message': 'Message posted successfully'}), 201

@posts_bp.route('/messages/<int:message_id>/like', methods=['POST'])
def like_message(message_id):
    """Increment the likes counter for a message"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE messages SET likes = likes + 1 
        WHERE message_id = %s
    """, (message_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Message liked successfully'}), 200