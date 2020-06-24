from flask import jsonify
import json

def api_response(message, status_code):

    """
    Function to jsonify response and return with the status code
    """
    response = jsonify(message)
    response.status_code = status_code
    return response

def invalid_usage(message, status_code, payload=None):

    rv = dict(payload or ())
    rv['message'] = message

    response = jsonify(rv)
    response.status_code = status_code
    return response




