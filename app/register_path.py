from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt
import secrets
import hashlib
import uuid

# creating a route named register
register_route = Blueprint('register', __name__)

# Connecto to the SQL Database
DB_HOST = 'db'
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'


def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn


def generateProfilePage(username, profileID):
    """
    This is being used to generate a simple profile page template for new users
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    bio = "Your Bio will go here, Max(100) character count"
    followers = []
    following = []
    myPosts = []
    pictureURL = '/getUpload/NoProfileImage.jpg'

    query = """
    INSERT INTO profilePages (profile_id, username, profilePictureUrl, bio, followers, following, MyPosts)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    cursor.execute(query, (profileID, username, pictureURL, bio, followers, following, myPosts))

    conn.commit()  
    cursor.close()
    conn.close()





@register_route.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # get the data from the json string sent from the front end
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirmpassword = data.get('confirmpassword')
        errors = {}

        # check to see if the username exists in (users)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        username_valid = True
        result = cursor.fetchone()
        if result:
            # user is taken and put false so we know its not valid so we can send a response
            errors['message2'] = 'username is taken'
            username_valid = False

        # checking to see if the password is valid
        valid1 = False
        valid2 = False
        # check if the created passwords match
        if password == confirmpassword:
            valid1 = True
        # create a way to check if the passowrd has a 8>=len, special char, digit, lower, upper
        ca, sm, sp, di = 0, 0, 0, 0
        capitalalphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        smallalphabets = "abcdefghijklmnopqrstuvwxyz"
        specialchar = "$@_!#$%&*()-_+=|/`~"
        digits = "0123456789"
        # count the stuff
        if len(password) >= 10:
            for character in password:
                if character in capitalalphabets:
                    ca += 1
                if character in smallalphabets:
                    sm += 1
                if character in specialchar:
                    sp += 1
                if character in digits:
                    di += 1
        if ca >= 1 and sm >= 1 and sp >= 1 and di >= 1 and ca + sm + sp + di == len(password):
            valid2 = True

        # send a bad respone if the password is not valid or the username is taken
        if valid1 == False or valid2 == False:
            errors['message1'] = 'invalid password'
        if valid1 == False or valid2 == False or username_valid == False:
            # so if any of valid is false we send an error message
            return jsonify(errors), 400
        else:
            # username and password is valid we put it into the database
            # hash the password
            salt = bcrypt.gensalt()
            db_salt = salt.decode('utf-8')
            hashed_password = bcrypt.hashpw(password.encode(), salt)
            db_password = hashed_password.decode('utf-8')
            # generate an unique cookie id and hash it loop till we get unique cookie
            token = secrets.token_urlsafe(16)
            hashed_token = hashlib.sha256(token.encode()).hexdigest()

            while True:
                cursor.execute('SELECT * FROM users WHERE cookie = %s', (hashed_token,))
                result = cursor.fetchone()
                if not result:
                    break
                token = secrets.token_urlsafe(16)
                hashed_token = hashlib.sha256(token.encode()).hexdigest()

            profile_id = uuid.uuid4()
            profile_id = str(profile_id)
            # put the username / password / token into the database
            cursor.execute('INSERT INTO users (username, profile_id, password, salt, cookie)  VALUES (%s, %s, %s, %s, %s)',
                           (username, profile_id, db_password, db_salt, hashed_token))
            
            #create the profile page
            generateProfilePage(username, profile_id)




            # the upload was successful
            conn.commit()
            cursor.close()
            conn.close()

            # Create the response
            response = make_response(jsonify({'message': 'Registration successful'}))

            # Set the session token in a secure cookie
            # set the unhashed cookie in this response

            response.set_cookie('session_token', token, httponly=True, secure=True, max_age=3600)
            # Return the response with the cookie
            return response

    # send the html code to the server
    return render_template('register.html')

