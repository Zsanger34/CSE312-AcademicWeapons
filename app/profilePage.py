from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt
from app.helper import *


get_Profile_Page_api = Blueprint('get_Profile_Page_api', __name__)

def getProfileDetail(profileID) -> dict:
    profileInfo = {"followers:": 0, "following": 0}

    return profileInfo


@get_Profile_Page_api.route('/profile/<path:profileID>', methods=['GET'])
def getProfilePage(profileID):

    try:
        profileInfo = getProfileDetail(profileID)
        return render_template('profilePage.html',
                                username=profileInfo['username'], 
                                BIO_GOES_HERE=profileInfo['bio'],
                                profilePictureUrl = profileInfo['profilePictureUrl'], 
                                Followers=profileInfo['followers'], 
                                Following=profileInfo['following'])
    except Exception:
        return render_template('404.html')
    


@get_Profile_Page_api.route('/profileEdit/<path:profileID>', methods=['POST'])
def editProfile(profileID):
    return None