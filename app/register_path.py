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
        #get the data information from the user
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        
        
        #check if the username is not in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()    #get the first matching row / user does exist
        print(f'does user exist?: {user}', flush=True)
        if user:
            #user does exist
            flash("Username already Exists. Please Create a New One!")
            return redirect(url_for('register'))
        
        #now if the user does exist we check the passwords match and hash it
        if password == confirmpassword:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
    #send the html code to the server 
    return render_template('register.html')

