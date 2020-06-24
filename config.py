import os

project_dir = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):

    HOST = "0.0.0.0"
    PORT = 5000

class DevelopmentConfig(Config):


    DEBUG = True

    HOST = "0.0.0.0"
    PORT = 5000
    USE_CELERY = True
    SECRET_KEY = "changeme"


class TestingConfig(Config):

    TESTING = True

    HOST = "0.0.0.0"
    PORT = 5000
    USE_CELERY = True
    SECRET_KEY = "changeme"


def get_config():

    env = os.getenv('FLASK_ENVIRONMENT', 'debug')
    config_obj = None

    if env.lower() == 'testing':
        config_obj = TestingConfig()
    elif env.lower() == "production":
        config_obj = ProductionConfig()
    else:
        config_obj = DevelopmentConfig()

    return config_obj
