from flask import Blueprint, request, jsonify, render_template, redirect, url_for, escape, make_response
import psycopg2
import hashlib

# Blueprint allows you to organize routes
logout_routes = Blueprint('logout', __name__)

# Database connection settings
DB_HOST = 'db'  
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

# Define the home route
@logout_routes.route('/logout', methods=['GET'])
def logout():
    
    #get the cookie information from the response
    session_token = request.cookies.get('session_token')
    hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
    
    #put an empty string into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET cookie = %s WHERE cookie = %s", ("", hashed_token))
    conn.commit()
    cursor.close()
    conn.close()
    
    #clear the cookie within the header
    response = make_response(redirect(url_for('register.register')))
    response.set_cookie('session_token', session_token, httponly=True, secure=True, max_age=-3600)
    return response
   

    