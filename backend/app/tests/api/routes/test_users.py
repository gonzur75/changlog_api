from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from app import handlers, schemas


def test_create_user(client: TestClient):
    test_json = {"username": "johndoe", "password": "password123"}
    response = client.post("/api/v1/users/", json=test_json)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "created_at" and "id" in data
    assert test_json["username"] == data["username"]


def test_sign_user_in(client: TestClient, session: Session):
    user_data = {"username": "jonedoe", "password": "secret123"}
    handlers.create_user(session, schemas.UserCreate(**user_data))
    response = client.post("/api/v1/signin/", data=user_data)

    assert response.status_code == 200, response.text
    assert "token" in response.text

    wrong_user_data = {"username": "jonedoe1", "password": "QQQQ"}
    response = client.post("/api/v1/signin/", data=wrong_user_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid credentials" in response.text
