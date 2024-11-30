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
    
    session_token = request.cookies.get('session_token')
    hashed_token = ''
    if not session_token:
        return redirect(url_for('login_page.login'))
    else: 
        hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE cookie = %s', (hashed_token,))
    username = cursor.fetchone()[0]
    valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    valid_inputs = True
    
    if request.method == 'POST':
        #getting the data and storing it into the database.
        data = request.get_json()
        action = data['action']
        if action == 'add':
            valid_inputs = True
            #missing inputs
            if not (data.get('day') or data.get('weight') or data.get('sets') or data.get('reps') or data.get('exerciseName')):
                response = make_response(jsonify({'error': 'missing inputs'}), 400)
                return response
            if data['day'] == '' or data['weight'] == '' or data['sets'] == '' or data['reps'] == '' or data['exerciseName'] == '':
                response = make_response(jsonify({'error': 'missing inputs'}), 400)
                return response
            
            #assign the values
            curr_day = str(data['day'])
            weight = str(data['weight'])
            sets = str(data['sets'])
            reps = str(data['reps'])
            exercise_name = str(data['exerciseName'])
            
            #check the values now
            if curr_day not in valid_days:
                response = make_response(jsonify({'error': 'invalid day'}), 400)
                return response
            if not (weight.isdigit() or sets.isdigit() or reps.isdigit()):
                response = make_response(jsonify({'error': 'invalid weight / sets / reps values '}), 400)
                return response
            if int(weight) < 0 or int(sets) < 0 or int(reps) < 0:
                response = make_response(jsonify({'error': 'invalid weight / sets / reps values'}), 400)
                return response
            if not exercise_name.replace(' ', '').replace('(', '').replace(')', '').replace('-', '').isalpha():
                response = make_response(jsonify({'error': 'exercise name'}), 400)
                return response
            
            #see if the exercise name already exists
            cursor.execute('SELECT * FROM addroutine WHERE username = %s and day = %s', (username,curr_day))
            workout_exists = cursor.fetchall()
            for exercise in workout_exists:
                if str(exercise[2]).lower() == exercise_name.lower():
                    response = make_response(jsonify({'error': 'exercise already exists'}), 400)
                    return response
            
            #adds each exercise into the database
            if valid_inputs:
                cursor.execute('INSERT INTO addroutine (username, day, name, weight, reps, sets) VALUES (%s, %s, %s, %s, %s, %s)',
                                (username, curr_day, exercise_name, weight, reps, sets))
                conn.commit()
        if action == 'remove':
            #check if the day is valid
            curr_day = str(data['day'])
            if curr_day not in valid_days:
                response = make_response(jsonify({'error': 'invalid day'}), 400)
                return response
            #check if the name is valid
            exercise_name = str(data['exerciseName'])
            if not exercise_name.replace(' ', '').replace('(', '').replace(')', '').replace('-', '').isalpha():
                response = make_response(jsonify({'error': 'exercise name'}), 400)
                return response
            cursor.execute('DELETE FROM addroutine WHERE username = %s and day = %s and name = %s', (username, data['day'], data['exerciseName']))
            conn.commit()
    
    #this is to collect all the workout information
    cursor.execute('SELECT * FROM addroutine WHERE username = %s', (username,))
    routine_data = cursor.fetchall()
    if not routine_data:
        routine_data = {}
    else:
        new_data = {}
        
        for exercise_row in routine_data:
            if new_data.get(exercise_row[1]):
                new_data[exercise_row[1]].append({'name': escape(exercise_row[2]), 'weight': escape(exercise_row[3]), 'reps': escape(exercise_row[4]), 'sets': escape(exercise_row[5])})
            else:
                new_data[exercise_row[1]] = [{'name': escape(exercise_row[2]), 'weight': escape(exercise_row[3]), 'reps': escape(exercise_row[4]), 'sets': escape(exercise_row[5])}]
                
        routine_data = new_data
    
    #this is for get      
    cursor.execute('SELECT * From addweek WHERE username = %s', (username,))
    workout_data = cursor.fetchall()
    dayData = []
    if workout_data:
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_in_list = []
        grouped_data = {day: [] for day in days_order}
        for row in workout_data:
            grouped_data[row[1]].append(list(row))
            days_in_list.append(row[1])
                
        dayData = [entry for day in days_order for entry in grouped_data[day]]
        
        cursor.close()
        conn.close()
    if request.method == 'POST':
        response = make_response(jsonify({'success': 'we are good', 'updated_list': routine_data}))
        return response
    else:
        return render_template('add_day.html', dayData=dayData, routineData=routine_data)
