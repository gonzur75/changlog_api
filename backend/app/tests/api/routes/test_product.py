from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import models, handlers, schemas
from app.modules.auth import create_jwt_token
from app.main import API_version_string


def get_test_auth_header(user_factory):
    user = user_factory()
    jwt_token = create_jwt_token(username=user.username)
    return {"Authorization": f"Bearer {jwt_token}"}


def test_retrieve_product(client: TestClient, session: Session, user_factory) -> None:
    headers = get_test_auth_header(user_factory)

    response_item_not_found = client.get(
        f"{API_version_string}products/1", headers=headers
    )
    assert response_item_not_found.status_code == 404
    assert "Product not found" in response_item_not_found.text

    user = session.query(models.User).first()
    print(user.id)
    another_user = user_factory(username="User X")

    product = schemas.ProductCreate(name="Product1")
    product2 = schemas.ProductCreate(name="Product2")

    user_product = handlers.create_product(session, product, user.id)
    another_user_product = handlers.create_product(session, product2, another_user.id)

    response_another_user_item = client.get(
        f"{API_version_string}products/{another_user_product.id}", headers=headers
    )
    assert response_another_user_item.status_code == 400
    assert "Not your product" in response_another_user_item.text

    response = client.get(
        f"{API_version_string}products/{user_product.id}", headers=headers
    )
    assert response.status_code == 200
    content = response.json()
    assert product.name in content.values()


def test_create_product(client: TestClient, user_factory) -> None:
    jwt_token_header = get_test_auth_header(user_factory)
    test_json = {"name": "composting.web"}
    response = client.post(
        f"{API_version_string}products/", headers=jwt_token_header, json=test_json
    )

    assert response.status_code == 200
    content = response.json()
    assert content["name"] == test_json["name"]
    assert "id" in content
    assert "owner_id" in content
