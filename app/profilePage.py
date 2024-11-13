from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt
from app.helper import *


get_Profile_Page_api = Blueprint('get_Profile_Page_api', __name__)

def getProfileDetail(profileID) -> dict:
    profileInfo = {}
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM profilePages WHERE profile_id = %s"

    cursor.execute(query, (profileID,))

    # Fetch the results (if any)
    result = cursor.fetchone()

    if result is not None:
        profileInfo = {
            'profile_id': result[0],
            'username': result[1],
            'profilePictureUrl': result[2],
            'bio': result[3],
            'followers': result[4],
            'following': result[5],
            'myPosts': result[6]
        }
    else:
        profileInfo = None


    cursor.close()
    conn.close()
    return profileInfo


@get_Profile_Page_api.route('/profile/<path:profileID>', methods=['GET'])
def getProfilePage(profileID):

    try:
        profileInfo = getProfileDetail(profileID)

        

        return render_template('profilePage.html',
                                username=profileInfo['username'], 
                                BIO_GOES_HERE=profileInfo['bio'],
                                profilePictureUrl = profileInfo['profilePictureUrl'], 
                                Followers=len(profileInfo['followers']), 
                                Following=len(profileInfo['following']),
                                FollowOrEdit="Edit")
    except Exception:
        return render_template('404.html')
    


@get_Profile_Page_api.route('/profileEdit/<path:profileID>', methods=['POST'])
def editProfile(profileID):
    return None