from flask import Blueprint, request, jsonify, render_template, flash, url_for, redirect
import psycopg2
import bcrypt


#creating a route named register
register_route = Blueprint('register', __name__)

#Connecto to the SQL Database
DB_HOST = 'db'  
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

@register_route.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        
        #get the data from the json string sent from the front end
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirmpassword = data.get('confirmpassword')
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
        
        #send a bad respone if the password is not valid
        errors = {}
        if valid1 == False or valid2 == False:
            errors['message1'] = 'invalid password'
            #errors['message2'] = 'username is taken'
            return jsonify(errors), 400
        else:
            #send a valid response if the password is valid
             return jsonify({'message': 'Password is Valid'}), 200
        
    #send the html code to the server 
    return render_template('register.html')

