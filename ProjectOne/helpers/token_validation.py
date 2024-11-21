from flask import request
import jwt
import app_config as config

def validate_jwt():
    token = None
    information = None
    
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    
    if not token:
        return 401
    
    try:
        information = jwt.decode(token, key = config.TOKEN_SECRET, algorithms = ["HS256"])
    except:
        return 403

    return information