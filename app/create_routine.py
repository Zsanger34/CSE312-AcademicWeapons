from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt


#create login route
add_week_route = Blueprint('addweek', __name__)

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
@add_week_route.route('/add_week', methods=['GET', 'POST'])
def workoutroutine():
    if request.method == 'POST':
        
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        #gathering the data which is the list, print(data, flush=True)
        #[{'day': 'Tuesday', 'title': 'i should be abnle to press enter'}, {'day': 'Monday', 'title': 'workout titel'}]
        data = request.get_json()
    
        if data is []:
            #if the data is empty
            print('send a bad response and make the user redo the form', flush=True)
            
        for day in data:
            if day['day'] not in valid_days:
                #if the day is not valid
                print('day is not valid', flush=True)
            
        #set up the database for inserting and checking
        print('success', flush=True)
            
        #if we pass the data is not empty and in the correct form and we pass the correct {} lets put it in the chat
        #table that contains all the users with workout cards
        
        #so put day, username, title -> in a database
        #if user is not in workout card table allow to create routine then add them to it after completion
        
        #go to add_add.html file where we will add the day

    return render_template('add_week.html')
