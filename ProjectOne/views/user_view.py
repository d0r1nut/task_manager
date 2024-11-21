from flask import Blueprint, jsonify, request
from database.__init__ import database
from models.user_model import User
from controllers.user_controller import create_user, login_user, fetch_users
from helpers.token_validation import validate_jwt


user = Blueprint("user", __name__)

@user.route('/users/signup', methods=['POST'])
def add_user():
    try:
        my_body = request.json

        if 'email' not in my_body:
            return jsonify({'error': 'Email is needed in the request!'}), 400
        if 'name' not in my_body:
            return jsonify({'error': 'Name is needed in the request!'}), 400
        if 'password' not in my_body:
            return jsonify({'error': 'Password is needed in the request!'}), 400

        my_user = User(my_body["name"], my_body["email"], my_body["password"])

        result = create_user(my_user)
        print(result)
        if result == "Duplicated User":
            return jsonify({'error': 'There is already an user with this email!'}), 400
        
        if not result.inserted_id:
            return jsonify({'error': 'Something wrong happened when creating user!'}), 500

        return jsonify({"id": str(result.inserted_id)})
    except:
        return jsonify({'error': 'Something wrong happened when creating user!'}), 500

@user.route('/users/login', methods=['POST'])
def login():
    try:
        my_body = request.json

        if 'email' not in my_body:
                return jsonify({'error': 'Email is needed in the request!'}), 400
        if 'password' not in my_body:
            return jsonify({'error': 'Password is needed in the request!'}), 400
        
        result = login_user(my_body)
        if result == 'Invalid Email':
            return jsonify({'error': 'Invalid Email or Password!'}), 400
        if result == 'Invalid Password':
            return jsonify({'error': 'Invalid Email or Password!'}), 400

        return login_user(my_body)
    except Exception as error:
        return jsonify({'error': 'Something wrong happened when login user!', 'error1': str(error)}), 500

@user.route('/users/all', methods=['GET'])
def get_users():
    try:
        token = validate_jwt()
        # print(token)
        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401

        return fetch_users()
    except:
        return jsonify({'error': 'Something wrong happened when fetching users!'}), 500

