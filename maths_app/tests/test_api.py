import json
from maths_app.models import User, guard


def test_login(client):
    response = client.post("/api/login", data=json.dumps({"username": "admin", "password": "admin"}))
    assert "token" in response.json.keys()


def test_current_user(client):
    with client.application.app_context():
        admin_user = User.lookup("admin")
        admin_header = guard.pack_header_for_user(admin_user)
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
    assert "token" in response.json.keys()
