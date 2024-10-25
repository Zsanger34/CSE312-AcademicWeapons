import hashlib

from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt

# create login route
get_post_api = Blueprint('get_post_api', __name__)
# Connecto to the SQL Database
DB_HOST = 'db'
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'


def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn


def validateUser(authToken):
    if not authToken:
        return False, None
    conn = get_db_connection()
    user = ""

    hash = hashlib.sha256()
    hash.update(authToken.encode('utf-8'))
    authTokenHashed = hash.hexdigest()

    cursor = conn.cursor()
    # check to see if the auth token is correct
    cursor.execute('SELECT * FROM users WHERE cookie = %s', (authTokenHashed,))
    result = cursor.fetchone()

    if result is None:
        cursor.close()
        conn.close()
        return (False, None)
    else:
        user = result[0]

    cursor.close()
    conn.close()
    return (True, user)
def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    # Id, What Message is, Like Counter
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    posts_organized = []
    for post in posts:
        format_post={"message_id": post[0],
            "message_content": post[2],
            "likes": post[3],
            "created_at": post[4].strftime('%Y-%m-%d %H:%M:%S')}
    return posts_organized


@get_post_api.route('/api/posts', methods=['GET'])
def get_all_posts():
    return jsonify(posts=get_posts())
