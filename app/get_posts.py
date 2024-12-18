import hashlib

from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt
from datetime import datetime, timedelta

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
            "created_at": time_ago(post[4]),
            "profile_id": post[5],
            "profile_picture_url": post[6]
        }
        posts_organized.append(format_post)
    return posts_organized


@get_post_api.route('/api/posts', methods=['GET'])
def get_all_posts():
    return jsonify(posts=get_posts())


def time_ago(post_time):
    
    now = datetime.now()
    diff = now - post_time
    
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