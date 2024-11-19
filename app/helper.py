from flask import Blueprint, request, jsonify, render_template, redirect, url_for, escape, make_response
import psycopg2
import hashlib
import os
import magic

# Database connection settings
DB_HOST = 'db'  
DB_NAME = 'mydatabase'
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'


def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn


def getProfileID(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT profile_id FROM users WHERE username = %s;"
    cursor.execute(query, (username))
    result = cursor.fetchone()

    conn.close()
    cursor.close()
    return result



def authticateUser(hashed_token):
    conn = get_db_connection()  
    cursor = conn.cursor()
    user = None
    userFound = None

    query = 'SELECT username FROM users WHERE cookie = %s'
    cursor.execute(query, (hashed_token,))
    user = cursor.fetchone()
    if user:
        userFound = True
        user = user[0]
    else:
        userFound = False
        user = None

    return (user, userFound)
