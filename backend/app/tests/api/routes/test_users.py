from starlette.testclient import TestClient


def test_create_user(client: TestClient):
    test_json = {"username": "johndoe", "password": "password123"}
    response = client.post("/api/v1/users/", json=test_json)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "created_at" and "id" in data
    assert test_json["username"] == data["username"]
