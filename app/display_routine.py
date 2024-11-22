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

#is the workout day
@workoutroutine_route.route('/workout_routine/<day>', methods=['GET'])
def workoutroutine(day):
    return render_template('workout_routine.html', username="njbousqu", day=day)


#is the workout week
@workoutroutine_route.route('/workout/<username>', methods=['GET'])
def workout(username):
    return render_template('workout.html', username=username)
