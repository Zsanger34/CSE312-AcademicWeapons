from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt


get_Profile_Page_api = Blueprint('get_Profile_Page_api', __name__)


