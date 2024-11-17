import hashlib

from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt

# create Post route
get_post_api = Blueprint('get_post_api', __name__)
# Connecton to the SQL Database
DB_HOST = 'db'
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn



def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Updated SQL query to join with profilePages table and retrieve profile_id and profilePictureUrl
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
        JOIN profilePages ON users.profile_id = profilePages.profile_id;
    """)

    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    posts_organized = []
    for post in posts:
        format_post = {
            "message_id": post[0],
            "username": post[1],
            "message_content": post[2],
            "likes": post[3],
            "created_at": post[4].strftime('%Y-%m-%d %H:%M:%S'),
            "profile_id": post[5],
            "profile_picture_url": post[6]
        }
        posts_organized.append(format_post)
    return posts_organized


@get_post_api.route('/api/posts', methods=['GET'])
def get_all_posts():
    return jsonify(posts=get_posts())
