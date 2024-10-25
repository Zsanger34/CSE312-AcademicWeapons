from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt


#create login route
addworkout = Blueprint('addworkout', __name__)

#Connecto to the SQL Database
DB_HOST = 'db'  
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'

#set up the database connection
def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

#get connection with the front-end with flask
@addworkout.route('/add_workout/', methods=['GET'])
def add():
    
    #using a list (monday, chest day)
    
    
   #its a form
    
    return render_template('add_workout.html')





#each link that directs them to this page will have an unqiue id. 
#look at melohub to check out

#CREATE TABLE days (username VARCHAR NOT NULL, day VARCHAR NOT NULL, workout_desc VARCHAR NOT NULL);