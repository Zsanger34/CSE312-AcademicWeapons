from flask import Blueprint, request, jsonify, render_template, make_response
from app.helper import *
import psycopg2
import bcrypt
import html



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
    # authToken = request.cookies.get("session_token", False)
    # if authToken == False:
    #     return render_template('404.html')
    
    # foundUser = validateUser(authToken)
    # if foundUser == False:
    #     return render_template('404.html')


    return render_template('settings.html')


@settings_routes.route('/settings/changePassword', methods=['POST'])
def changePassword():

    #check if the user is a valid user
    (userFound, user) = validateUser(authToken)
    if userFound == False:
        return make_response(render_template('404.html'), 404)


    #retrieve all the needed data
    data = request.get_json()
    confirmOldPassword = data.get("confirmOldPassword", False)
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


    #now obtain the proper information to change the password
    cursor.execute('SELECT * FROM users WHERE username = %s', (user,))
    result = cursor.fetchone()

    
    # check if the old password is the same as the password in the database
    dataBasePassword = result[1]
    salt = result[2]

    hashedConfrimPassword = bcrypt.hashpw(confirmOldPassword.encode(), salt.encode('utf-8'))

    if hashedConfrimPassword != dataBasePassword:
        #return an error saying that the old password do not match and try again
        cursor.close()
        conn.close()
        return jsonify({"errorMessage": "old password is incorrect"}), 400
    else:
        #check to see if the newPasswords meets the criteria and also check if the 
        (validPasswordCheck, message) = validatePassword(newPassword, confirmNewPassword)

        if validPasswordCheck == False:
            #return a response saying there was something wrong with the new passwords and use the given message
            cursor.close()
            conn.close()
            return jsonify({"errorMessage": message}), 400
        
        else:
            #make the change in the database and return a 200 ok, with the message saying the passwords has been changed
            newSalt = bcrypt.gensalt()
            hashNewPassword = bcrypt.hashpw(newPassword, newSalt)
            cursor.execute("UPDATE users SET password = %s AND salt = %s WHERE username = %s", (hashNewPassword, newSalt, user))

            #send a 200 ok response
            cursor.close()
            conn.close()
            response = make_response(jsonify({'message': message}))
            return response







@settings_routes.route('/settings/changeUserName', methods=['POST'])
def changeUserName():

    #check if the user is a valid user
    (userFound, user) = validateUser(authToken)
    if userFound == False:
        return jsonify({"errorMessage": "You are not properly authorized"}), 403

    data= request.get_json()
    oldUserName = data.get("oldUserName", False)
    newUserName = data.get("newUserName", False)
    newUserName = html.escape(newUserName)
    authToken = request.cookies.get("session_token", False)

    #first check if we were able to obtain all the data we need
    if oldUserName == False or newUserName == False:
        return
    

    #check to see if the old username matches what is stored in the database
    if oldUserName != user:
        return make_response(jsonify({'errorMessage': "OldUsername did not match current username"})), 400
    

    #since it matches update the user's username
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("UPDATE users SET username = %s WHERE username = %s", (newUserName, oldUserName))

    con.close()
    cursor.close()

    return make_response(jsonify({"message": "username Updated Succesfully"})), 200
    
    

