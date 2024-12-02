from flask import Blueprint, request, jsonify
from app.helper import *

Follow_User_api = Blueprint('Follow_User_api', __name__)


@Follow_User_api.route("/profile/followUser", methods=['POST'])
def followUser():
    session_token = request.cookies.get('session_token')
    if not session_token:
        return jsonify({"errorMessage": "session token was not found, reload the page"})
    else: 
        hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
        username, userFound = authticateUser(hashed_token)
    
    if userFound == False:
        return jsonify({"errorMessage": "no user was found"}), 400


    #check for any data was sent
    chosenUser = request.form.get('chosenUser')
    if chosenUser == None:
        return jsonify({'errorMessage': 'no data was sent'}), 400
    

    if chosenUser == username:
        return jsonify({'errorMessage': 'cant follow yourself'}), 400


    #check if the user being followed is actually a user
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT EXISTS (SELECT 1 FROM users WHERE username = %s)"
    cursor.execute(query, (chosenUser,))
    exists = cursor.fetchone()[0]

    if exists == False:
        cursor.close()
        conn.close()
        return jsonify({"errorMessage":"The user you wanted to follow can not be found"}), 400
    

    

    #check to see if the user is already following this user
    query = """
    SELECT p.following
    FROM users u
    JOIN profilePages p ON u.profile_id = p.profile_id
    WHERE u.cookie = %s;
    """
    cursor.execute(query, (hashed_token,))

    results = cursor.fetchone()
    if results:
        followingList = results[0]

    if chosenUser in followingList:
        cursor.close()
        conn.close()
        return jsonify({'errorMessage': "you are already following this user"}), 400
    

    add_user_query = """
    UPDATE profilePages
    SET following = array_append(following, %s)
    WHERE username = %s AND NOT (%s = ANY (following));
    """
    cursor.execute(add_user_query, (chosenUser, username, chosenUser))


    add_user_query = """
    UPDATE profilePages
    SET followers = array_append(followers, %s)
    WHERE username = %s AND NOT (%s = ANY (followers));
    """
    cursor.execute(add_user_query, (username, chosenUser, username))


    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"goodMessage": f'Successfully followed {chosenUser}'}), 200



@Follow_User_api.route("/profile/unFollowUser", methods=['POST'])
def unFollowUser():
    session_token = request.cookies.get('session_token')
    if not session_token:
        return jsonify({"errorMessage": "session token was not found, reload the page"})
    else: 
        hashed_token = hashlib.sha256(session_token.encode()).hexdigest()
        username, userFound = authticateUser(hashed_token)
    
    if userFound == False:
        return jsonify({"errorMessage": "no user was found"}), 400


    #check for any data was sent
    chosenUser = request.form.get('chosenUser')
    if chosenUser == None:
        return jsonify({'errorMessage': 'no data was sent'}), 400
    

    if chosenUser == username:
        return jsonify({'errorMessage': 'cant unfollow yourself'}), 400
    

    #check if the user being unfollowed is actually a user
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT EXISTS (SELECT 1 FROM users WHERE username = %s)"
    cursor.execute(query, (chosenUser,))
    exists = cursor.fetchone()[0]

    if exists == False:
        cursor.close()
        conn.close()
        return jsonify({"errorMessage":"The user you want to unfollow can not be found"}), 400



    #check to see if the user is already not being following this user
    query = """
    SELECT p.following
    FROM users u
    JOIN profilePages p ON u.profile_id = p.profile_id
    WHERE u.cookie = %s;
    """
    cursor.execute(query, (hashed_token,))

    results = cursor.fetchone()
    if results:
        followingList = results[0]

    if chosenUser not in followingList:
        cursor.close()
        conn.close()
        return jsonify({'errorMessage': "you are already following this user"}), 400






    #unfollow the user
    remove_user_query = """
    UPDATE profilePages
    SET following = array_remove(following, %s)
    WHERE username = %s;
    """
    cursor.execute(remove_user_query, (chosenUser, username))



    remove_user_query = """
    UPDATE profilePages
    SET followers = array_remove(followers, %s)
    WHERE username = %s;
    """
    cursor.execute(remove_user_query, (username, chosenUser))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'goodMessage': f'unfollowed {chosenUser}'}), 200