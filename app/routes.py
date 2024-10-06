from flask import Blueprint, request, jsonify, render_template
import psycopg2

# Blueprint allows you to organize routes
main_routes = Blueprint('main', __name__)

# Database connection settings
DB_HOST = 'db'  
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

# Define the home route
@main_routes.route('/')
def home():
    return render_template('index.html')

