import datetime
import flask
import jwt
from flask import request, jsonify
from flask_cors import cross_origin

SECRET_KEY="python_jwt"



def encode_func():
    json_data = request.json
    json_data['date']= str(datetime.datetime.now())
    encode_data = jwt.encode(payload=json_data,key=SECRET_KEY, algorithm="HS256")
    return encode_data


def decode_func():
    try:
        decode_data = None
        headers = flask.request.headers
        bearer = headers.get('Authorization')
        token = bearer.split()[1]
        try:
            decode_data = jwt.decode(jwt=token, key=SECRET_KEY, algorithms="HS256")
        except Exception as e:
            print(f"Token is Invalid {e}")
        old_time_obj = datetime.datetime.strptime(decode_data['date'], '%Y-%m-%d %H:%M:%S.%f')
        current_time_obj = datetime.datetime.now()
        if old_time_obj.hour - current_time_obj.hour >= 10:
            return {"Error": "The token has expired please login again"}, token
        return decode_data, token
    except Exception as e:
        return "invalid token"



