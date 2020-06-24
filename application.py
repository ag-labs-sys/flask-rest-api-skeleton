from flask import Flask, request, Response, jsonify
import json
import os
from flask_swagger_ui import get_swaggerui_blueprint

def create_application():

    # main flask application
    application = Flask(__name__)

    from config import DevelopmentConfig, TestingConfig

    env = os.getenv('FLASK_ENVIRONMENT', 'debug')

    if env.lower() == 'testing':
        application.config.from_object(TestingConfig())
    else:
        application.config.from_object(DevelopmentConfig())

    # registering blueprints
    from api.v1 import tasks
    application.register_blueprint(tasks.blueprint, url_prefix='/api/v1/tasks')

    ### swagger specific ###
    SWAGGER_URL = '/swagger'
    SWAGGER_FILE = '../static/swagger.json'
    swagger_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        SWAGGER_FILE,
        config={
            'app_name': "flask-api"
        }
    )
    application.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    ### end swagger specific ###


    @application.route("/")
    def hello():

        message = {
            'status': 200,
            'message': 'API V1.0 IS LIVE ',
        }

        response = Response(json.dumps(message), status=200, mimetype='application/json')
        return response

    @application.errorhandler(404)
    def not_found(error=None):
        message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404

        return resp

    return application

if __name__ == "__main__":

    application = create_application()
    application.run(host=application.config['HOST'], port=application.config['PORT'], threaded=True)
