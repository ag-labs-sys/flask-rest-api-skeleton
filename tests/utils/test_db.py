import unittest
from tests.tests import BaseTest
import pytest
import json

from datetime import datetime
from models.task import Task


class TestDatabase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def app_client(
            self,
            db_session
    ):

        self.db_session = db_session

    def test_create_retrieve_task(self):
        timestamp = datetime.now()
        timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")

        task = Task(id="1234", text = "hello", timestamp=timestamp)
        current_count = self.db_session.add(task)
        assert current_count == 1

        task = self.db_session.get_task("1234")
        assert task is not None

