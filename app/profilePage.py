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

        editOrFollow = "Follow"
        function = "followUser()"

        print("testing", flush=True)
        session_token = request.cookies.get('session_token')
        if not session_token:
            print("no token")
            return redirect(url_for('login_page.login'))
        else: 
            hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
            username, userFound = authticateUser(hashed_token)
            
            if userFound == False:
                return redirect(url_for('login_page.login'))

            print(profileInfo['username'], flush=True)
            print(username, flush=True)
            if profileInfo['username'] == username:
                
                function = "editPage()"
                editOrFollow = "Edit"
        
        UserPosts = getUsersPosts(username, profileInfo['profilePictureUrl'], profileID)
        return render_template('profilePage.html',
                                username=profileInfo['username'], 
                                BIO_GOES_HERE=profileInfo['bio'],
                                profilePictureUrl = profileInfo['profilePictureUrl'], 
                                Followers=len(profileInfo['followers']), 
                                Following=len(profileInfo['following']),
                                followOrEditFunction = function,
                                FollowOrEdit=editOrFollow,
                                posts=UserPosts)
    except Exception:
        return render_template('404.html')
    


@get_Profile_Page_api.route('/verifyUser', methods=['GET'])
def verifyUser():
    session_token = request.cookies.get('session_token')
    if not session_token:
        print("no token")
        return jsonify({"verified": False})
    else: 
        hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
        username, userFound = authticateUser(hashed_token)

    if userFound == False:
        print("user was not found")
        return jsonify({"verified": False})

    return jsonify({"verified": True})







@get_Profile_Page_api.route('/profileEdit/<path:profileID>', methods=['POST'])
def editProfile(profileID):
    return None




#@get_Profile_Page_api.route('/profile/<profile_id>/getPosts', methods=['GET'])
def getUsersPosts(username, profilePictureUrl, profileID):
    conn = get_db_connection()
    cursor = conn.cursor()
    #get the posts
    query = """
    SELECT messages.message_id, 
       messages.message_content, 
       messages.likes, 
       messages.created_at
    FROM messages
    JOIN users ON messages.user_id = users.id
    WHERE users.profile_id = %s
    ORDER BY messages.created_at ASC;
    """
    cursor.execute(query, (profileID,))
    messages = cursor.fetchall()

    posts = []

    for message in messages:
        newPost = {
            'profilePictureUrl': profilePictureUrl,
            'username': username,
            'profileURL': profileID,
            'POSTCONTENT': message[1],
            'POSTLIKECOUNTER': message[2],
            'POSTTIME': message[3]
        }
        posts.append(newPost)

    cursor.close()
    conn.close()
    return posts