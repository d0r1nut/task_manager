from flask import Blueprint, jsonify, request
from models.task_model import Task
from controllers.task_controller import create_task, fetch_created_tasks, fetch_assigned_tasks, get_task_by_id, update_task_db, delete_task_db
from controllers.user_controller import get_user_by_uid, get_user_by_email
from helpers.token_validation import validate_jwt


task = Blueprint("task", __name__)

@task.route('/tasks/add', methods=['POST'])
def add_task():
    try:
        my_body = request.json
        # print(my_body)
        token = validate_jwt()

        if token == 401:
            return jsonify({'error': 'Token is missing in the request, please try again!'}), 401
        if token == 403:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 403
        
        if 'description' not in my_body:
            raise ValueError('Description is needed in the request!')
        if 'assignedToUid' not in my_body:
            raise ValueError('AssignedToUid is needed in the request!')
        
        createdby_user = get_user_by_email(token["email"])
        assignedto_user = get_user_by_uid(my_body["assignedToUid"])

        if assignedto_user == None or createdby_user == None:
            return jsonify({'error': 'User not found!'}), 400
        
        new_task = Task(token["id"], createdby_user["name"], my_body["assignedToUid"], assignedto_user["name"], my_body["description"])
        result = create_task(new_task)

        if result == "Duplicated Task":
            return jsonify({'error': 'There is already a task with this description!'}), 400
        if not result.inserted_id:
            return jsonify({'error': 'Something wrong happened when creating task!'}), 500

        return jsonify({"id": str(result.inserted_id)})
    except ValueError as err: 
        return jsonify({"error": str(err)}), 400 

@task.route('/tasks/<task_uid>', methods=['PATCH'])
def update_task(task_uid):
    try:
        token = validate_jwt()

        if token == 401:
            return jsonify({'error': 'Token is missing in the request, please try again!'}), 401
        if token == 403:
            return jsonify({'error': 'Invalid authentication token, please login again'}), 403
        body = request.json

        if 'data' not in body:
            return jsonify({"error": 'No data found in the request'}), 400 

        data = body["data"]
        user = get_user_by_email(token["email"])
        task = get_task_by_id(task_uid)

        if task == None:
            raise Exception('Task not found') 
        if str(user["_id"]) != task["assignedToUid"]:
            raise Exception('Users can only change status when task is assigned to them.')
        print(data)

        update_task_db(task_uid, data)
        
        return jsonify({"task_uid": task_uid})
    except Exception as error:
        return jsonify({'error': 'Something wrong happened when updating task!', 'error_desc': str(error)}), 500

@task.route('/tasks/<task_uid>', methods=['GET'])
def get_task(task_uid):
    try:
        token = validate_jwt()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401

        task = get_task_by_id(task_uid)
        return task
    except:
        return jsonify({'error': 'Something wrong happened when fetching tasks!'}), 500

@task.route('/tasks/createdby', methods=['GET'])
def get_created_tasks():
    try:
        token = validate_jwt()
        # print(token)
        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token, please login again!'}), 401

        return fetch_created_tasks()
    except:
        return jsonify({'error': 'Something wrong happened when fetching tasks!'}), 500

@task.route('/tasks/assignedto', methods=['GET'])
def get_assigned_tasks():
    try:
        token = validate_jwt()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401

        return fetch_assigned_tasks()
    except:
        return jsonify({'error': 'Something wrong happened when fetching tasks!'}), 500
    
@task.route('/tasks/<task_uid>', methods=['DELETE'])
def delete_task(task_uid):
    try:
        token = validate_jwt()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401

        user = get_user_by_email(token["email"])
        task = get_task_by_id(task_uid)

        if task == None:
            raise Exception('Task not found')
        
        if str(user["_id"]) != task["createdByUid"]:
            raise Exception('Users can only delete when task is created by them.')
        
        taskDeleteAttempt = delete_task_db(task_uid)
        
        return jsonify({'tasksAffected': taskDeleteAttempt.deleted_count}), 200
    except:
        return jsonify({'error': 'Something wrong happened when deleting tasks!'}), 500
