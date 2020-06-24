from flask import Blueprint
from flask_restful import Api

from controllers.task_controller import Task, TaskList


blueprint = Blueprint('tasks', __name__)

api = Api(blueprint)
api.add_resource(Task, '/<string:uuid>')
api.add_resource(TaskList, '/')


