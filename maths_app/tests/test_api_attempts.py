import json
from maths_app.models import User, guard
from . import utils


def test_attempt_test(client_sample_q):
    # TODO: Attempt trig test
    # Steps:
    # 1. Post to api/tests/attempt
    # 2. Return first question information
    # 3. Post answer
    # 4. Return next question information
    # 5. Post answer
    # 6. Return notification that all questions have been answered and return attempt information again
    # This will now have the percentage correct and if it was pass/fail
    pass


def test_attempts(client_attempts):
    # TODO: With a completed attempt
    # 1. Endpoint /api/tests/<id>/attempts
    # Show all attempts of a test and if the student/passed/failed
    pass
