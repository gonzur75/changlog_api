from starlette.testclient import TestClient

from app.modules.auth import create_jwt_token
from app.main import API_version_string


def get_token_for_test(user_factory):
    user = user_factory()
    jwt_token = create_jwt_token(username=user.username)
    return {"Authorization": f"Bearer {jwt_token}"}


def test_create_product(client: TestClient, user_factory) -> None:
    jwt_token_header = get_token_for_test(user_factory)
    test_json = {"name": "composting.web"}
    content = client.post(
        f"{API_version_string}products/", headers=jwt_token_header, json=test_json
    )

    assert content.status_code == 200
    content = content.json()
    assert content["name"] == test_json["name"]
    assert "id" in content
    assert "owner_id" in content
