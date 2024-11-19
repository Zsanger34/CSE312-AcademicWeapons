from flask import Blueprint, request, jsonify, render_template, make_response, current_app
from app.helper import *
import os
from werkzeug.utils import secure_filename
import uuid

UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

get_Profile_Page_api = Blueprint('get_Profile_Page_api', __name__)


@get_Profile_Page_api.route('/profile/<path:profileID>', methods=['GET'])
def getProfilePage(profileID):
    try:
        profileInfo = getProfileDetail(profileID)

        editOrFollow = "Follow"
        function = "followUser()"

        session_token = request.cookies.get('session_token')
        if not session_token:
            print("no token")
            return redirect(url_for('login_page.login'))
        else: 
            hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
            username, userFound = authticateUser(hashed_token)
            
            if userFound == False:
                return redirect(url_for('login_page.login'))

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
    



@get_Profile_Page_api.route('/profile/profileEdit', methods=['POST'])
def editProfile():
    #check to see if this is the correct user that is editing the profile page
    session_token = request.cookies.get('session_token')
    if not session_token:
        return jsonify({"errorMessage": "session token was not found, reload the page"})
    else: 
        hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
        username, userFound = authticateUser(hashed_token)
    
    if userFound == False:
        return jsonify({"errorMessage": "no user was found"})
    



    conn = get_db_connection()
    cursor = conn.cursor()
    #now check that this is the correct user changing the profilePage
    newBio = request.form.get('bio', '')
    newPicture = request.files.get('profileImage')

    #check if no data was sent
    if newBio == '' and newPicture == None:
        return jsonify({"errorMessage": "no Data was Sent"})
    

    if newBio == '': #only the profile picture is being changed
        (updated, message) = uploadNewProfilePicture(conn, cursor, newPicture, username)
        if updated == False:
            return jsonify({"errorMessage": message}), 400
        cursor.close()
        conn.close()
        return jsonify({"pictureChanged": True, "newPictureURL": message}), 200
    elif newPicture == None: #only the bio is being changed

        #check to see if the new bio is over 100 characters
        if len(newBio) > 100:
            cursor.close()
            conn.close()
            return jsonify({"errorMessage": "Bio length is too Long"}), 400
        
        
        query = "UPDATE profilePages SET bio = %s WHERE username = %s"
        cursor.execute(query, (newBio, username))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"bioChanged": True, "newBio": newBio}), 200
    
    else:
        updated, results = uploadNewProfilePicture(conn, cursor, newPicture, username)
        if updated == False:
            return jsonify({"errorMessage": results})

        #check to see if the new bio is over 100 characters
        if len(newBio) > 100:
            cursor.close()
            conn.close()
            return jsonify({"errorMessage": "Bio length is too Long"}), 400
        
        query = "UPDATE profilePages SET bio = %s WHERE username = %s"
        cursor.execute(query, (newBio, username))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"bioAndPicture": True, "newBio": newBio, "newPictureURL": results}), 200
    


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

    postsSwapped = posts[::-1]
    cursor.close()
    conn.close()
    return postsSwapped








def uploadNewProfilePicture(conn, cursor, newPicture, username):
    FILESIGNATURES = ['image/jpeg', 'image/png', 'image/jpg']
    uploadFolder = current_app.config['UPLOAD_FOLDER']

    #get the MIME type and check to see if its the correct file allowed
    MimeType = getFileType(newPicture)
    if MimeType not in FILESIGNATURES:
        errorMessage = "This file is not allowed"
        return False, errorMessage 
    
    fileExtension = MimeType.split('/', 1)[1]
    #check to see if the file does not exist
    filename = f"{uuid.uuid4().hex}.{fileExtension}"
    newPath = f'{uploadFolder}{filename}'

    #save the new path to for the profile
    query = "UPDATE profilePages SET profilePictureUrl = %s WHERE username = %s"
    cursor.execute(query, (newPath, username))
    conn.commit()

    return True, None