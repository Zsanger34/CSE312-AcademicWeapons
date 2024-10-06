from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import psycopg2

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
@main_routes.route('/')
def home():
    
    session_token = request.cookies.get('session_token')
    if not session_token:
        return redirect(url_for('register.register'))
    # Query the database for the user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE cookie = %s', (session_token,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        # Pass the username to the template
        return render_template('index.html', username=user[0])
    else:
        return redirect(url_for('register.register'))

