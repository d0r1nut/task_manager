from flask import jsonify
from database.__init__ import database
import app_config as config
import bcrypt
from helpers.token_validation import validate_jwt
from bson import ObjectId

def generate_hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password

def create_task(task):
    try:
        task.description = task.description.lower()
        task.assignedToUid = task.assignedToUid.lower()

        # print(task.__dict__)

        collection = database.database[config.CONST_TASK_COLLECTION]
        if collection.find_one({'description': task.description}):
            return "Duplicated Task"
        
        return collection.insert_one(task.__dict__)
    except:
        raise Exception("Error on creating task!")
    
def get_task_by_id(task_id):
    try:
        collection = database.database[config.CONST_TASK_COLLECTION]
        task = collection.find_one({'_id': ObjectId(task_id)})
        task['_id'] = str(task['_id'])
        return task
    except:
        raise Exception("Error on fetching task!")
    
def fetch_created_tasks():
    try:
        token_uid = validate_jwt().get('id')
        collection = database.database[config.CONST_TASK_COLLECTION]
        tasks = []
        for task in collection.find({'createdByUid': token_uid}):
            current_task = {
                'id': str(task['_id']),
                'assignedToUid': task['assignedToUid'],
                'assignedToName': task['assignedToName'],
                'description': task['description'],
                'createdByUid': task['createdByUid'],
                'createdByName': task['createdByName'],
                'done': task['done']
            }
            tasks.append(current_task)
        
        return jsonify({'tasks': tasks})
    except:
        raise Exception("Error on fetching task!")
    
def fetch_assigned_tasks():
    try:
        token_uid = validate_jwt().get('id')
        collection = database.database[config.CONST_TASK_COLLECTION]
        tasks = []
        for task in collection.find({'assignedToUid': token_uid}):
            current_task = {
                'id': str(task['_id']),
                'assignedToUid': task['assignedToUid'],
                'assignedToName': task['assignedToName'],
                'description': task['description'],
                'createdByUid': task['createdByUid'],
                'createdByName': task['createdByName'],
                'done': task['done']
            }
            tasks.append(current_task)
        
        return jsonify({'tasks': tasks})
    except:
        raise Exception("Error on fetching task!")
    
def update_task_db(task_id, data):
    try:
        collection = database.database[config.CONST_TASK_COLLECTION]
        collection.update_one({'_id': ObjectId(task_id)}, {'$set': {"done": data['done'], "description": data['description']}})
    except:
        raise Exception("Error on updating task!")
    
def delete_task_db(task_id):
    try:
        collection = database.database[config.CONST_TASK_COLLECTION]
        taskDeleteAttempt = collection.delete_one({'_id': ObjectId(task_id)})
        return taskDeleteAttempt
    except:
        raise Exception("Error on deleting task!")