import pytest
from application import create_application
from models.task import Task, TaskSchema
import uuid
from datetime import datetime


@pytest.fixture(scope="session")
def application_client():

    application = create_application()
    application.config['TESTING'] = True
    client = application.test_client()
    return client

@pytest.fixture(scope="session")
def header():

    header = {
        "Content-Type": "application/json"
    }
    return header

@pytest.fixture(scope="function")
def task(db_session):

    unique_id = uuid.uuid1()
    timestamp = datetime.now()  # current date and time
    timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")

    text = "hello"

    task = TaskSchema().load({"text": text, "id": unique_id, "timestamp": timestamp})
    db_session.add(task)

    yield TaskSchema().dump(task)

