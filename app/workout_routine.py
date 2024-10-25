from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt


#create login route
workoutroutine_route = Blueprint('workoutroutine', __name__)

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
@workoutroutine_route.route('/workout_routine/<day>', methods=['GET'])
def workoutroutine(day):
    #get the day / username
    #display the muscle groups associated with the [username, day]
    #1.) to get the the exercises to display in each muscle group [username, day, muscle_group]
        #-> this will return a list and then just populate the list which will be a list for each mucle group e.g (bench press, chest flies)
    
    
   
    return render_template('workout_routine.html', username="njbousqu", day=day)




#CREATE TABLE exercise (username VARCHAR NOT NULL, day VARCHAR NOT NULL, musclegroup VARCHAR NOT NULL, name VARCHAR NOT NULL, sets INT, reps INT, weight INT);
#CREATE TABLE muscle (musclegroup VARCHAR NOT NULL, username VARCHAR NOT NULL, day VARCHAR NOT NULL);