import json

import pytest

from . import utils


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


@pytest.mark.xfail(reason="Should students only be allowed one active attempt?", raises=AssertionError)
def test_attempt_blocked(client_sample_q):
    auth_header_student = utils.get_user_header(client_sample_q, "jsmith")

    # Get and pick out the first test the student can see
    all_tests = client_sample_q.get("/api/tests", headers=auth_header_student).json

    active_test = all_tests[0]

    # Post to initiate an attempt
    response = client_sample_q.post("/api/tests/{}/attempts".format(active_test["id"]), headers=auth_header_student)
    assert response.status_code == 201
    assert "id" in response.json.keys()

    # Post to initiate an attempt again (Should be blocked)
    response = client_sample_q.post("/api/tests/{}/attempts".format(active_test["id"]), headers=auth_header_student)
    assert response.status_code == 400

    # Post to initiate an attempt on another test (Should be blocked)
    response = client_sample_q.post("/api/tests/{}/attempts".format(all_tests[1]["id"]), headers=auth_header_student)
    assert response.status_code == 400


@pytest.mark.xfail(reason="Should this be interpreted as the student correcting their choice or disallowed with a 400",
                   raises=AssertionError)
def test_duplicate_answer(client_sample_q):
    auth_header_student = utils.get_user_header(client_sample_q, "jsmith")

    # Get and pick out the first test the student can see
    all_tests = client_sample_q.get("/api/tests", headers=auth_header_student).json

    active_test = all_tests[0]

    # Post to initiate an attempt
    response = client_sample_q.post("/api/tests/{}/attempts".format(active_test["id"]), headers=auth_header_student)
    assert response.status_code == 201
    attempt_id = response.json["id"]

    response = client_sample_q.get("/api/tests/{}/questions".format(active_test["id"]), headers=auth_header_student)
    test_questions = response.json

    endpoint = "/api/tests/{}/attempts/{}/answer".format(active_test["id"], attempt_id, test_questions[0]["id"])
    answer = {"option_id": test_questions[0]["options"][0]["id"]}
    response = client_sample_q.post(endpoint, data=json.dumps(answer), headers=auth_header_student)
    assert response.status_code == 201
    response = client_sample_q.post(endpoint, data=json.dumps(answer), headers=auth_header_student)
    assert response.status_code == 400


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

    # Check that the teacher can see the attempt
    auth_header_teacher = utils.get_user_header(client_sample_q, "stiger")
    response_teacher = client_sample_q.get("/api/tests/{}/attempts".format(active_test["id"]),
                                           headers=auth_header_teacher)
    print(response_teacher.json)
    assert response_teacher.json[0]["mark"] == response.json["mark"]
