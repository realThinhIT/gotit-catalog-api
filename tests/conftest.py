import pytest

from main import app
from main.database import db
from tests.helpers import create_mock_data, drop_tables


@pytest.fixture
def session():
    # Create app context
    app.app_context().push()

    # Create the database and the database table
    db.create_all()

    # Import mock data
    create_mock_data()

    yield app

    # In the next call drop all data in the databases
    drop_tables()


@pytest.fixture
def client(session):
    testing_client = session.test_client()

    yield testing_client
