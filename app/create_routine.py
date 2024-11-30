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
    
    #setup
    conn = get_db_connection()
    cursor = conn.cursor()
    session_token = request.cookies.get('session_token')
    hashed_token = ''
    if not session_token:
        return redirect(url_for('login_page.login'))
    else: 
        hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
        
    cursor.execute('SELECT username FROM users WHERE cookie = %s', (hashed_token,))
    user = cursor.fetchone()
    username = escape(user[0])
    
    #get data or send data
    if request.method == 'POST':
        
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data = request.get_json()
        action = data['action']
        
        if data['day'] not in valid_days:
            return jsonify({'error': 'you did not upload a valid day'}), 400
        
        #remove / add a day from the llist
        if action == 'remove':
            cursor.execute('DELETE FROM addweek WHERE username = %s and day = %s', (username, data['day']))
            cursor.execute('DELETE FROM addroutine WHERE username = %s and day = %s', (username, data['day']))
            conn.commit()
        if action == 'add':
            if not data['title'].replace(' ', '').replace('(', '').replace(')', '').replace('-', '').isalpha():
                return jsonify({'error': 'title contains invalid characters'}), 400
            cursor.execute('SELECT * FROM addweek WHERE username = %s and day = %s', (username, data['day']))
            get_day = cursor.fetchone()
            if get_day:
                return jsonify({'error': 'day already exists'}), 400
            
            cursor.execute('INSERT INTO addweek (username, day, title) VALUES (%s, %s, %s)',
                (username, data['day'], data['title']))
            conn.commit()
    
    #see if user has created a workout yet
    cursor.execute('SELECT * FROM addweek WHERE username = %s', (username,))
    user_table = cursor.fetchall()
    routine_list = []
    if user_table:
        for row in user_table:
            routine_list.append({'day': escape(row[1]), 'title': escape(row[2])})
    cursor.close()
    conn.close()
    
    if request.method == 'POST':
        response = make_response(jsonify({'success': 'we are good', 'updated_list': routine_list}))
        return response
    
    return render_template('add_week.html', workout_days=routine_list)
    