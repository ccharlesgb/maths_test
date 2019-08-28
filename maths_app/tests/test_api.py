import json


def test_login(client):
    response = client.get("/api/login", data=json.dumps({"username": "admin", "password": "admin"}))
    assert "token" in response.json.keys()
