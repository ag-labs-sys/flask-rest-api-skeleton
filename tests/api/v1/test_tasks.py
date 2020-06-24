import unittest
from tests.tests import BaseTest
import pytest
import json
from datetime import datetime
import uuid

API_PREFIX = '/api/v1/tasks/'



class TestTaskAPI(BaseTest, unittest.TestCase):

    @pytest.fixture(autouse=True)
    def app_client(
            self,
            application_client,
            header,
            db_session,
            task
    ):

        """
        Fixture to set up objects for use between all tests
        :param application_client:
        :param header:
        :return: None
        """

        self.application_client = application_client
        self.header = header
        self.db_session = db_session
        self.task = task

    def create_task(self, data):

        res = self.application_client.post(
            "{}".format(API_PREFIX),
            headers=self.header,
            data=json.dumps(data)
        )

        return res

    def generate_new_task_id(self):

        return uuid.uuid1()

    def test_task_add(self):
        """
        test the creation of a task with some text
        :param application_client:
        :param header:
        :return:
        """
        text = "Hello. I am Task 1"
        data = {"text": text}

        res = self.create_task(data)

        response_data = json.loads(res.data)
        assert 'id' in response_data
        assert 'text' in response_data
        assert 'timestamp' in response_data
        assert res.status_code == 201

    def test_task_add_empty(self):
        """
        test the creation of a task with empty text.
        should throw error with a 422 status code
        """

        text = ""
        data = {"text": text}

        res = self.application_client.post(
            "{}".format(API_PREFIX),
            headers=self.header,
            data=json.dumps(data)
        )

        response_data = json.loads(res.data)
        assert response_data['status'] == 'INVALID TEXT'
        assert res.status_code == 400


    def test_task_retrieve_valid(self):

        print()
        task_id = self.task['id']
        res = self.application_client.get(
            "{}{}".format(API_PREFIX, task_id),
            headers=self.header
        )

        response_data = json.loads(res.data)
        assert response_data['id'] == task_id
        assert res.status_code == 200


    def test_task_retrieve_invalid_id(self):

        uuid = self.generate_new_task_id()
        res = self.application_client.get(
            "{}{}".format(API_PREFIX, uuid),
            headers=self.header
        )

        response_data = json.loads(res.data)
        assert 'status' in response_data and response_data['status'] == "ERROR"
        assert res.status_code == 404


    def test_task_delete(self):

        """
        create new task and test it's deletion
        :param application_client:
        :param header:
        :return:
        """

        task = self.task

        res = self.application_client.delete(
            "{}{}".format(API_PREFIX, task['id']),
            headers=self.header
        )

        response_data = json.loads(res.data)
        assert res.status_code == 200
        assert response_data['status'] == 'DELETED'


        get_response = self.application_client.get(
            "{}{}".format(API_PREFIX, task['id']),
            headers=self.header
        )
        response_data = json.loads(get_response.data)
        assert get_response.status_code == 404


    def test_task_update(self):

        task = self.task

        timestamp = datetime.now()  # current date and time
        timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        new_task_data = {
            "uuid" : task['id'],
            "text" : task['text'] + " udpated",
            "timestamp" : timestamp
        }


        res = self.application_client.put(
            "{}{}".format(API_PREFIX, task['id']),
            headers=self.header,
            data=json.dumps(new_task_data)
        )


        response_data = json.loads(res.data)
        assert res.status_code == 200
        assert response_data['status'] == 'UPDATED'

        res = self.application_client.get(
            "{}{}".format(API_PREFIX, task['id']),
            headers=self.header
        )

        task = json.loads(res.data)
        assert res.status_code == 200
        assert task['text'] == new_task_data['text']


    def test_creating_retrieval_multiple_tasks(self):

        """
        create a number of tasks and retrieve all
        :param application_client:
        :param header:
        :return:
        """
        self.db_session.clear()
        tasks = []
        for i in range(4):

            data = {"text" : "Task {}".format(i+1)}
            tasks.append("Task {}".format(i+1))
            res = self.create_task(data)

            response_data = json.loads(res.data)
            assert 'text' in response_data
            assert res.status_code == 201



        get_all_response = self.application_client.get(
            "{}".format(API_PREFIX),
            headers=self.header
        )
        assert get_all_response.status_code == 200
        response_data = json.loads(get_all_response.data)
        print("Response data = {}".format(response_data))
        for task in response_data:
            assert task['text'] in tasks
