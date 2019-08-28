import pytest
from maths_app import create_app
from maths_app.utils import init_db, create_user


@pytest.fixture
def client():
    app_config = {"APP_DATABASE": 'sqlite://', "APP_SECRET_KEY": "jadjas9as"}
    app = create_app(app_config)

    with app.app_context():
        init_db()
        create_user("stiger", "1234", "teacher", "Scott Tiger", "scott.tiger@mail.com")
        create_user("jsmith", "1234", "student", "John Smith", "john.smith@mail.com")

    app.testing = True
    test_client = app.test_client()

    yield test_client
