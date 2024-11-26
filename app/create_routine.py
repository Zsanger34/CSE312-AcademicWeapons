from flask import Blueprint, request, jsonify, render_template, redirect, url_for, escape, make_response
import psycopg2
import hashlib



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
    conn = get_db_connection()
    cursor = conn.cursor()
    errors = {}

    session_token = request.cookies.get('session_token')
    hashed_token = ''
    if not session_token:
        return redirect(url_for('login_page.login'))
    else: 
        hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
    cursor.execute('SELECT username FROM users WHERE cookie = %s', (hashed_token,))
    user = cursor.fetchone()
    username = escape(user[0])
    
    #see if user has created a workout yet
    cursor.execute('SELECT * FROM addweek WHERE username = %s', (username,))
    user_table = cursor.fetchall()
    if user_table:
        errors['error'] = 'unsuccessful'
        errors['message'] = 'user already has table'
        return jsonify(errors), 400
    
    if request.method == 'POST':
        
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data = request.get_json()
    
        if data is []:
            errors['error'] = 'unsucessful'
            return jsonify(errors), 400
            
        for day in data:
            if day['day'] not in valid_days:
                errors['error'] = 'unsucessful'
                return jsonify(errors), 400
            else:
                cursor.execute('INSERT INTO addweek (username, day, title) VALUES (%s, %s, %s)',
                           (username, day['day'], day['title']))
                conn.commit()
                
        cursor.close()
        conn.close()
        
        response = make_response(jsonify({'success': 'we are good'}))
        return response

    return render_template('add_week.html')
