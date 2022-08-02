import pytest

from app import create_app
from app.models import User
from config import TestConfig


@pytest.fixture(scope="module")
def new_user():
    user = User(
        email_address="mash@example.com",
        password="8wCS0H65r@p!8%B0XxrPTbBiR%^tc##f",
        timezone="Europe/London",
    )
    return user


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(config_class=TestConfig)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
