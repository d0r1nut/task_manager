from flask import jsonify
from database.__init__ import database
import app_config as config
import bcrypt
from datetime import datetime, timedelta
import jwt

def generate_hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password

def create_user(user):
    try:
        user.name =  user.name.lower()
        user.email = user.email.lower()
        user.password = generate_hash_password(user.password)

        print(user.__dict__)

        collection = database.database[config.CONST_USER_COLLECTION]

        if collection.find_one({'email': user.email}):
            return "Duplicated User"

        return collection.insert_one(user.__dict__)
    except:
        raise Exception("Error on creating user!")

def login_user(user_information):
    try:
        email = user_information["email"].lower()
        password = user_information["password"].encode("utf-8")

        collection = database.database[config.CONST_USER_COLLECTION]

        current_user = collection.find_one({'email': email})

        if not current_user:
            return "Invalid Email"
        
        if not bcrypt.checkpw(password, current_user["password"]):
            return "Invalid Password"

        expiration = datetime.utcnow() + timedelta(seconds = config.JWT_EXPIRATION)
        jwt_data = {'email': current_user['email'], 'id': str(current_user['_id']), 'exp': expiration}

        jwt_to_return = jwt.encode(payload = jwt_data, key = config.TOKEN_SECRET)

        logged_user = {
            'id': str(current_user['_id']),
            'email': current_user['email'],
            'name': current_user['name'],
        }
        
        return jsonify({'token': jwt_to_return, 'expiration': config.JWT_EXPIRATION, 'logged_user': logged_user})
    except Exception as error:
        print(error)
        raise Exception("Error on login user!")
    
def fetch_users():
    try:
        collection = database.database[config.CONST_USER_COLLECTION]
        users = []
        for user in collection.find():
            current_user = {
                'id': str(user['_id']),
                'email': user['email'],
                'name': user['name']
            }
            users.append(current_user)
        
        return jsonify({'users': users})
    except:
        raise Exception("Error on fetching user!")
    
def get_user_by_uid(uid):
    try:
        res = None
        collection = database.database[config.CONST_USER_COLLECTION]
        for user in collection.find():
            if str(user['_id']) == uid:
                res = user
                break
        return res if res else None
    except:
        raise Exception("Error on fetching user!")

def get_user_by_email(email):
    try:
        collection = database.database[config.CONST_USER_COLLECTION]
        user = collection.find_one({'email': email})
        return user if user else None
    except:
        raise Exception("Error on fetching user!")