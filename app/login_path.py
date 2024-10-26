from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt
import secrets
import hashlib

# create login route
login_route = Blueprint('login_page', __name__)

# Connecto to the SQL Database
DB_HOST = 'db'
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'


# set up the database connection
def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn


# get connection with the front-end with flask
@login_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # gathering the data submitted from the frontend
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        errors = {}

        # check if the usename exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()
        if result:
            # user exists within the code

            # check if the password entered matches the password in the table
            cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
            database_password = cursor.fetchone()[0]

            # get the password and salt and hash the current password
            cursor.execute('SELECT salt FROM users WHERE username = %s', (username,))
            salt = cursor.fetchone()[0]
            bytes_salt = salt.encode('utf-8')
            hashed_password = bcrypt.hashpw(password.encode(), bytes_salt)

            # compare the two passwords not to make sure they are the same
            if database_password.encode('utf-8') != hashed_password:
                # the passwords do not match return an error message
                cursor.close()
                conn.close()
                errors['message1'] = 'Password is Not Valid'
                return jsonify(errors), 400
            else:
                # the passwords do match

                # generate an unique cookie id and hash it loop till we get unique cookie
                token = secrets.token_urlsafe(16)
                hashed_token = hashlib.sha256(token.encode()).hexdigest()

                # update the cookie
                cursor.execute("UPDATE users SET cookie = %s WHERE username = %s", (hashed_token, username))
                conn.commit()

                cursor.close()
                conn.close()
                # Create the response
                response = make_response(jsonify({'message': 'Registration successful'}))
                # Set the session token in a secure cookie
                response.set_cookie('session_token', token, httponly=True, secure=True, max_age=3600)
                # Return the response with the cookie
                return response

        else:
            # username does not exist and returns an error message to the frontend
            cursor.close()
            conn.close()
            errors['message'] = 'Username is Not Valid'
            return jsonify(errors), 400

    return render_template('login.html')