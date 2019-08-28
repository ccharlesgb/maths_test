import pytest
from maths_app import create_app


@pytest.fixture
def client():
    app_config = {"APP_DATABASE": 'sqlite://', "APP_SECRET_KEY": "jadjas9as"}
    app = create_app(app_config)
    app.testing = True
    test_client = app.test_client()

    yield test_client
