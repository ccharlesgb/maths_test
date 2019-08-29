import pytest
from maths_app import create_app, db, models
from maths_app.utils import init_db, create_user
from .utils import generate_test_question
from itertools import chain


def _get_base_app():
    app_config = {"APP_DATABASE": 'sqlite://', "APP_SECRET_KEY": "jadjas9as"}
    app = create_app(app_config)

    with app.app_context():
        init_db()
        create_user("stiger", "1234", "teacher", "Scott Tiger", "scott.tiger@mail.com")
        create_user("jsmith", "1234", "student", "John Smith", "john.smith@mail.com")

    app.testing = True
    return app


@pytest.fixture
def client():
    """
    Barebones client with minimal database for app to work
    """
    app = _get_base_app()
    test_client = app.test_client()
    yield test_client


@pytest.fixture
def client_sample_q():
    """
    Client with built-in tests and questions
    """
    app = _get_base_app()
    tests = []
    tests.append(models.Test(name="Algebra", pass_fraction=0.5, enabled=False))
    tests.append(models.Test(name="Trig", pass_fraction=0.8, enabled=True))
    tests.append(models.Test(name="Trig 2", pass_fraction=0.8, enabled=True))

    questions = []
    questions.append(generate_test_question("Q 1", 3, 1, test=tests[0]))
    questions.append(generate_test_question("Q 2", 3, 1, test=tests[0]))
    questions.append(generate_test_question("Q 3", 4, 1, test=tests[1]))
    questions.append(generate_test_question("Q 4", 2, 1, test=tests[1]))
    questions.append(generate_test_question("Q 5", 6, 3, test=tests[1]))
    questions.append(generate_test_question("Q 6", 3, 1, test=tests[2]))

    with app.app_context():
        db.session.add_all(chain(tests, questions))
        db.session.commit()

    test_client = app.test_client()
    yield test_client
