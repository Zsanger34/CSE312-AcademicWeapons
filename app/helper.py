from flask import Blueprint, request, jsonify, render_template, make_response
import psycopg2
import bcrypt



def validatePassword(password, confirmpassword):
    #checking to see if the password is valid
    valid1 = False
    valid2 = False
    #check if the created passwords match
    if password == confirmpassword:
        valid1 = True
    #create a way to check if the passowrd has a 8>=len, special char, digit, lower, upper
    ca, sm, sp, di = 0, 0, 0, 0
    capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smallalphabets="abcdefghijklmnopqrstuvwxyz"
    specialchar="$@_!#$%&*()-_+=|/`~"
    digits="0123456789"
    #count the stuff
    if len(password) >= 10:
        for character in password:
            if character in capitalalphabets:
                ca += 1
            if character in smallalphabets:
                sm += 1
            if character in specialchar:
                sp += 1
            if character in digits:
                di += 1
    if ca >= 1 and sm >= 1 and sp >= 1 and di >= 1 and ca+sm+sp+di==len(password):
        valid2 = True

    if valid1 == False:
        return (False, "both passwords do not match")
    
    if valid2 == False:
        return (False, "passwords do not meet the criteria")
    
    return (True, "both passwords are the same and meet the criteria")




def validateUser(authToken):

    return True