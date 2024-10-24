from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt
import hashlib


#Connecto to the SQL Database
DB_HOST = 'db'  
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn


def validatePassword(password, confirmpassword):
    #checking to see if the password is valid
    valid1 = False
    valid2 = False
    #check if the created passwords match
    if password == confirmpassword:
        valid1 = True
    #create a way to check if the passowrd has a 8>=len, special char, digit, lower, upper
    ca, sm, sp, di = 0, 0, 0, 0
    capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smallalphabets="abcdefghijklmnopqrstuvwxyz"
    specialchar="$@_!#$%&*()-_+=|/`~"
    digits="0123456789"
    #count the stuff
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
    if ca >= 1 and sm >= 1 and sp >= 1 and di >= 1 and ca+sm+sp+di==len(password):
        valid2 = True

    if valid1 == False:
        return (False, "both passwords do not match")
    
    if valid2 == False:
        return (False, "passwords do not meet the criteria")
    
    return (True, "both passwords are the same and meet the criteria")




def validateUser(authToken):
    conn = get_db_connection()
    user = ""

    hash = hashlib.sha256()
    hash.update(authToken.encode('utf-8'))
    authTokenHashed = hash.hexdigest()

    cursor = conn.cursor()
    #check to see if the auth token is correct
    cursor.execute('SELECT * FROM users WHERE cookie = %s', (authTokenHashed,))
    result = cursor.fetchone()

    if result is None:
        return (False, None)
    else:
        user = result[0]
    


    return (True, user)