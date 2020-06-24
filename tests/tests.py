import unittest
from abc import ABCMeta
import pytest
from utils.db import DBSessionProvider


@pytest.mark.usefixtures()
class BaseTest(unittest.TestCase):

    __metaclass__ = ABCMeta


    @classmethod
    def setUpClass(cls):

        pass

    def setUp(self):
        pass

    def tearDown(self):
        """
        This function is called after ever test in a class to clear the data created by the test
        :return:
        """
        pass

    @classmethod
    def tearDownClass(cls):
        pass
