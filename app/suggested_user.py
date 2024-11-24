import hashlib

from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt

# Connecton to the SQL Database
DB_HOST = 'db'
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'

get_sug_user_api = Blueprint('get_sug_user_api', __name__)
def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn


@get_sug_user_api.route('/sugusers', methods=['GET'])
def get_sug_user():
    conn = get_db_connection()
    cursor = conn.cursor()

    session_token = request.cookies.get('session_token')
    hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
    cursor.execute('SELECT id FROM users WHERE cookie = %s', (hashed_token,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "Invalid session token"}), 403

    user_id = user[0]

    cursor.execute("""
            SELECT profilePages.profile_id, users.username, profilePages.profilePictureUrl
            FROM users
            JOIN profilePages ON users.profile_id = profilePages.profile_id
            WHERE users.id != %s
            ORDER BY RANDOM()
            LIMIT 5;

        """, (user_id,))

    profiles = cursor.fetchall()
    cursor.close()
    conn.close()
    sug_users = []

    for profile in profiles:
        sug_users.append({
            "profile_id": profile[0],
            "username": profile[1],
            "profile_picture_url": profile[2]
        })

        return jsonify(sug_users=sug_users)
