
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, escape, make_response, current_app, send_from_directory
import os
import psycopg2
import hashlib
from app.helper import *

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


def getProfileID(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT profile_id FROM users WHERE username = %s;"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    profile_id = None
    if result is not None:
        profile_id = result[0]  
    else:
        profileLink = "not-found"

    conn.close()
    cursor.close()
    return profile_id


# Define the home route
@main_routes.route('/', methods=['GET', 'POST'])
def home():
    
    #get the cookie if the user is logged in
    #the token is going to be plain text
    session_token = request.cookies.get('session_token')
    if not session_token:
        return redirect(url_for('login_page.login'))
    else: 
        hashed_token = hashlib.sha256(session_token.encode()).hexdigest()



    # check to see if we got a post request.
    if request.method == "POST":
        #the user is logged out and now we clear the cookie token
        response = make_response(jsonify({'message': 'Registration successful'}))
        response.set_cookie('session_token', session_token, httponly=True, secure=True, max_age=-3600)
        return response

    # Query the database for the user if user is logged in get their information
    #hash the token taken from the session_token above code to look up the users info
    #hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE cookie = %s', (hashed_token,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        # Pass the username to the template
        username = escape(user[0])
        profile_id = getProfileID(username)
        profileLink = "profile/" + profile_id


        return render_template('index.html', username=username, profileURL= profileLink)
    else:
        return redirect(url_for('register.register'))






#this route will be used to request all the images uploaded to the app
#all upload files will be obtain from this route which will auto set the MIME Type for us
#But it checks the file extension so make sure the file extension is correct
import mimetypes
@main_routes.route('/getUpload/<upload>', methods=["GET"])
def getUpload(upload):
    file_path = os.path.join('static/uploads', upload)
    try:
        mimeType, discard = mimetypes.guess_type(file_path)
        return send_from_directory('static/uploads', upload, mimetype=mimeType)
    except FileNotFoundError:
        return "File not found", 404
