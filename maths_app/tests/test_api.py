import json


def test_login(client):
    response = client.post("/api/login", data=json.dumps({"username": "admin", "password": "admin"}))
    assert "token" in response.json.keys()
