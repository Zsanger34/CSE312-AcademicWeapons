from flask import Blueprint, request, jsonify, render_template, redirect, url_for, escape, make_response
import psycopg2
import hashlib



#create login route
add_day_route = Blueprint('add_day', __name__)

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
@add_day_route.route('/add_day', methods=['GET', 'POST'])
def day_routine():
    
    if request.method == 'POST':
        response = make_response(jsonify({'success': 'we are good'}))
        return response

    return render_template('add_day.html')
