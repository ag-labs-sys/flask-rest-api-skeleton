from flask_restful import Resource, reqparse
from flask import request, jsonify
from models.task import TaskSchema
import uuid
from marshmallow import ValidationError
from utils.db import db_session
from datetime import datetime
from utils.utils import api_response
from utils.utils import invalid_usage

def get_current_timestamp():

    timestamp = datetime.now()  # current date and time
    timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
    return timestamp

def is_task_id_valid(task_id):

    task = db_session.get_task(task_id)
    if task is None:
        return False
    else:
        return True


class Task(Resource):

    """Single object resource
    """

    def get(self, uuid):

        task = db_session.get_task(uuid)
        if task is None:

            payload = {
                'status': 'ERROR'
            }
            return invalid_usage('No task exists with this ID', 404, payload )

        task_schema = TaskSchema()
        task_json = task_schema.dump(task)

        return api_response(task_json, 200)


    def put(self, uuid):

        data = request.json
        id = uuid
        task = db_session.get_task(id)

        if task is None:

            # return error that no contact exists with this username
            message = {
                'status': 404,
                'errors': 'No task exists with this ID'
            }

            resp = jsonify(message)
            resp.status_code = 404
            return resp

        data['timestamp'] = get_current_timestamp()
        db_session.update_task(id, data)
        task = db_session.get_task(id)

        return api_response(
            {'status': 'UPDATED', 'message':'Task updated'}, 200
        )



    def delete(self, uuid):

        if db_session.get_task(uuid) is not None:

            deleted = db_session.delete_task(uuid)
            if deleted == True:
                return api_response({'status' : 'DELETED', 'message':'Task deleted'}, 200)
            else:
                return api_response({"status" : "NOT DELETED", 'message' : "Task not found"}, 404)

        else:

            message = {
                'status': "NOT DELETED",
                'errors': 'No task exists with this ID'
            }

            resp = jsonify(message)
            resp.status_code = 404
            return resp


class TaskList(Resource):

    """Creation and get_all
    """

    def get(self):

        # return all tasks stored in memory

        tasks = db_session.get_all_tasks()
        task_schema = TaskSchema(many=True)
        task_json_res = task_schema.dump(tasks)

        response = jsonify(task_json_res)
        response.status_code = 200
        return response


    def post(self):

        task_data = request.json
        task_text = task_data['text']

        if task_text == "":
            return invalid_usage("Text for task cannot be empty", 400, {"status" : "INVALID TEXT"})

        unique_id = uuid.uuid1()
        timestamp = get_current_timestamp()

        # validate text data and other data
        try:

            task = TaskSchema().load({"text": task_data['text'], "id": unique_id, "timestamp" : timestamp})
            db_session.add(task)

            json_task = TaskSchema().dump(task)
            response = jsonify(json_task)
            response.status_code = 201
            return response

        except ValidationError as err:

            error_message = err.messages
            error_validation = err.valid_data

            response = jsonify(error_message)
            response.status_code = 422
            return response
