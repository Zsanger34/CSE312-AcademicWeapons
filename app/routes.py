from flask import Blueprint, request, jsonify, render_template, redirect, url_for, escape, make_response
import psycopg2
import hashlib

# Blueprint allows you to organize routes
main_routes = Blueprint('main', __name__)

# Database connection settings
DB_HOST = 'db'  
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

# Define the home route
@main_routes.route('/', methods=['GET', 'POST'])
def home():
    
    #get the cookie if the user is logged in
    #the token is going to be plain text
    session_token = request.cookies.get('session_token')
    if not session_token:
        return redirect(url_for('register.register'))

    # Query the database for the user if user is logged in get their information
    #hash the token taken from the session_token above code to look up the users info
    #hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
    cursor.execute('SELECT username FROM users WHERE cookie = %s', (hashed_token,))
    user = cursor.fetchone()
    if user is None:
        return redirect(url_for('register.register'))
    cursor.close()
    conn.close()
    if user:
        # Pass the username to the template
        username = escape(user[0])
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('register.register'))

