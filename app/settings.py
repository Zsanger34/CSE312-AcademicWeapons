from flask import Blueprint, request, jsonify, render_template, make_response
from helper import *
import psycopg2
import bcrypt



#create login route
settings_routes = Blueprint('settings_page', __name__)

#Connecto to the SQL Database
DB_HOST = 'db'  
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'

#set up the database connection
def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn


@settings_routes.route('/settings', methods=['GET'])
def settingsPage():
    return render_template('settings.html')


@settings_routes.route('/settings/changePassword', methods=['POST'])
def changePassword():
    #retrieve all the needed data
    data = request.get_json()
    confirmOldPassword = data.get("confirmPassword", False)
    newPassword = data.get("newPassword", False)
    confirmNewPassword = data.get("confirmNewPassword", False)
    authToken = request.cookies.get("session_token", False)

    if confirmOldPassword == False or newPassword == False or confirmNewPassword == False:
        #all the data was not sent return a error response
        return

    if authToken == False:
        #return a response saying there was an issue with the auth token
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    #check to see if the auth token is correct
    cursor.execute('SELECT * FROM users WHERE cookie = %s', (authToken,))
    result = cursor.fetchone()

    if result is None:
        #This means that the auth Token is wrong and return an error 403 response
        return jsonify({"errorMessage": "You are not properly autherized"}), 403
    
    # check if the old password is the same as the password in the database
    username = result[0]
    dataBasePassword = result[1]
    salt = result[2]

    hashedConfrimPassword = bcrypt.hashpw(confirmOldPassword.encode(), salt.encode('utf-8'))

    if hashedConfrimPassword != dataBasePassword:
        #return an error saying that the old password do not match and try again
        return jsonify({"errorMessage": "old password is incorrect"}), 400
    else:
        #check to see if the newPasswords meets the criteria and also check if the 
        (validPasswordCheck, message) = validatePassword(newPassword, confirmNewPassword)

        if validPasswordCheck == False:
            #return a response saying there was something wrong with the new passwords and use the given message
            return jsonify({"errorMessage": message}), 400
        
        else:
            #make the change in the database and return a 200 ok, with the message saying the passwords has been changed
            response = make_response(jsonify({'message': message}))
            return response







@settings_routes.route('/settings/changeUserName', methods=['POST'])
def changeUserName():
    data= request.get_json()
    oldUserName = data.get("oldUserName", False)
    newUserName = data.get("newUserName", False)