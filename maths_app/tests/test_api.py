import json
from maths_app.models import User, guard
from . import utils


def test_login(client):
    response = client.post("/api/login", data=json.dumps({"username": "admin", "password": "admin"}))
    assert response.status_code == 201
    assert "token" in response.json.keys()


def test_current_user(client):
    admin_header = utils.get_user_header(client, "admin")
    response = client.get("/api/current_user", headers=admin_header)
    assert response.json["username"] == "admin"


def test_register_user(client):
    user = "new_student"
    password = "pass1"
    user_data = {"username": user,
                 "password": password,
                 "email": "test@mail.com",
                 "full_name": "New Student"}
    response = client.post("/api/register", data=json.dumps(user_data))

    assert "id" in response.json.keys()

    # Test that we can now log in with these credentials
    response = client.post("/api/login", data=json.dumps({"username": user, "password": password}))
    assert response.status_code == 201
    assert "token" in response.json.keys()


def test_create_test(client):
    auth_header = utils.get_user_header(client, "stiger")  # Teacher Auth
    test_data = {"name": "Algebra",
                 "pass_fraction": 0.5}
    response = client.post("/api/test", data=json.dumps(test_data), headers=auth_header)
    assert response.status_code == 201
    assert "id" in response.json.keys()


def test_toggle_test_enable(client):
    auth_header = utils.get_user_header(client, "stiger")  # Teacher Auth
    test_data = {"name": "Algebra",
                 "pass_fraction": 0.5,
                 "enabled": 1}
    response = client.post("/api/test", data=json.dumps(test_data), headers=auth_header)

    auth_header = utils.get_user_header(client, "stiger")  # Teacher Auth
    response = client.patch("/api/test/{}".format(response.json["id"]), headers=auth_header)
    assert response.status_code == 200
    assert "disabled" in response.json["message"]


def test_create_test_student(client):
    auth_header = utils.get_user_header(client, "jsmith")  # Student Auth
    test_data = {"name": "Algebra",
                 "pass_fraction": 0.5}
    response = client.post("/api/test", data=json.dumps(test_data), headers=auth_header)
    assert response.status_code == 403


def test_get_test_disabled_student(client):
    pass


def test_create_question(client):
    auth_header = utils.get_user_header(client, "stiger")  # Teacher Auth
    test_data = {"name": "Algebra",
                 "pass_fraction": 0.5}
    test_id = client.post("/api/test", data=json.dumps(test_data), headers=auth_header).json["id"]

    question_data = {"body": "What is 1+1?",
                     "options": [{"value": "0", "correct": False},
                                 {"value": "1", "correct": False},
                                 {"value": "2", "correct": True}]}
    end_point = "/api/test/{0:}/question".format(test_id)
    response = client.post(end_point, data=json.dumps(question_data), headers=auth_header)
    assert response.status_code == 201

    response = client.get(end_point + "/{}".format(response.json["id"]), headers=auth_header)
    # TODO: Compare the json more strictly here using some kind of testing util
    assert response.json["body"] == question_data["body"]
    assert len(question_data["options"]) == len(question_data["options"])
