from flask import Blueprint, request, jsonify, render_template
import psycopg2

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
        
        return jsonify({
            "username": username,
            "password": password,
            "confirmpassword": confirmpassword
        }), 200
        
    #send the html code to the server 
    return render_template('register.html')

