import json
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


def test_promote_user(client):
    user = "new_teacher"
    password = "pass2"
    user_data = {"username": user,
                 "password": password,
                 "email": "test@mail.com",
                 "full_name": "New Teacher"}
    response = client.post("/api/register", data=json.dumps(user_data))
    teacher_id = response.json["id"]

    admin_header = utils.get_user_header(client, "admin")
    print("/api/users/{}".format(teacher_id))
    response = client.patch("/api/users/{}".format(teacher_id), data=json.dumps({"role": "teacher"}),
                            headers=admin_header)
    assert "promoted" in response.json["message"]

    jwt_response = client.post("/api/login", data=json.dumps({"username": user, "password": password}))
    jwt_header = {"Authorization": "Bearer " + jwt_response.json["token"]}
    
    # Test teacher protected route
    test_data = {"name": "Algebra",
                 "pass_fraction": 0.5}
    response = client.post("/api/tests", data=json.dumps(test_data), headers=jwt_header)
    assert response.status_code == 201
