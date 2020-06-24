import pytest
from utils.db import DBSessionProvider

@pytest.fixture(scope="function")
def db_session():
    """
    db session fixture
    :return:
    """

    db_session = DBSessionProvider.get_db_session()

    yield db_session

    # executed at teardown
    db_session.clear()
