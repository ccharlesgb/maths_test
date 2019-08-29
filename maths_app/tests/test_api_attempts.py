import json
from maths_app.models import User, guard
from . import utils
import pytest


def test_start_attempt_test(client_sample_q):
    auth_header_student = utils.get_user_header(client_sample_q, "jsmith")

    # Get and pick out the first test the student can see
    all_tests = client_sample_q.get("/api/tests", headers=auth_header_student).json

    active_test = all_tests[0]

    # Check we can't see this tests questions yet
    response = client_sample_q.get("/api/tests/{}/questions".format(active_test["id"]), headers=auth_header_student)
    assert response.status_code == 404

    # Post to initiate an attempt
    response = client_sample_q.post("/api/tests/{}/attempts".format(active_test["id"]), headers=auth_header_student)
    assert response.status_code == 201
    assert "id" in response.json.keys()
    attempt_id = response.json["id"]

    # Check we can see the questions now
    response = client_sample_q.get("/api/tests/{}/questions".format(active_test["id"]), headers=auth_header_student)
    assert response.status_code == 200

    # Check we can't see the other tests questions
    other_test = all_tests[1]
    response = client_sample_q.get("/api/tests/{}/questions".format(other_test["id"]), headers=auth_header_student)
    assert response.status_code == 404


@pytest.mark.parametrize("test_name,target_marks", [
    ("Trig", 2), ("Trig 2", 1), ("Trig 2", 0)
])
def test_complete_test(client_sample_q, test_name, target_marks):
    auth_header_student = utils.get_user_header(client_sample_q, "jsmith")

    # Get and pick out Trig 2 as this only has 1 question
    all_tests = client_sample_q.get("/api/tests", headers=auth_header_student).json
    active_test = list(filter(lambda elem: elem["name"] == test_name, all_tests))[0]
    # Start an attempt and get the questions
    response = client_sample_q.post("/api/tests/{}/attempts".format(active_test["id"]),
                                    headers=auth_header_student)
    attempt_id = response.json["id"]

    # TODO: The student can see the correct answer while they still has an active attempt
    # TODO: Probably should do this after the attempt is closed
    response = client_sample_q.get("/api/tests/{}/questions".format(active_test["id"]), headers=auth_header_student)
    test_questions = response.json

    expected_marks = 0
    for question in test_questions:
        # Pick first correct id if we are below our target mark
        if expected_marks < target_marks:
            option_id = [elem["id"] for elem in question["options"] if elem["correct"]][0]
            expected_marks += 1
        else:  # otherwise pick the wrong answer
            option_id = [elem["id"] for elem in question["options"] if not elem["correct"]][0]
        answer = {"option_id": option_id}

        endpoint = "/api/tests/{}/attempts/{}/answer".format(active_test["id"], attempt_id, question["id"])
        response = client_sample_q.post(endpoint, data=json.dumps(answer), headers=auth_header_student)
        assert response.status_code == 201

    response = client_sample_q.get("/api/tests/{}/attempts/{}".format(active_test["id"], attempt_id),
                                   headers=auth_header_student)
    # Check that we got the expected amount of marks
    assert response.json["completed_utc"] is not None
    assert response.json["mark"] == expected_marks
