import factory
from starlette.testclient import TestClient

from app import schemas
from app.main import API_version_string
from app.tests.utils import get_test_auth_header_and_user


def test_modify_update(
    client: TestClient, user_factory, product_factory, update_factory
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory(owner=user)
    update = update_factory(product=product)

    json = {"title": "New Title"}
    response = client.patch(
        f"{API_version_string}updates/{update.id}", headers=headers, json=json
    )
    assert response.status_code == 200
    content = schemas.Update(**response.json())
    assert content.title == json["title"]
    assert content.updated_at != content.created_at


def test_retrieve_update(
    client: TestClient, user_factory, update_factory, product_factory
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory(owner=user)
    update = update_factory(product=product)

    response = client.get(f"{API_version_string}updates/{update.id}", headers=headers)
    print(response.text)
    assert response.status_code == 200
    content = schemas.Update(**response.json())
    assert content.id == update.id


def test_create_update(
    client: TestClient, user_factory, update_factory, product_factory
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory(owner=user)

    data = factory.build(dict, FACTORY_CLASS=update_factory)
    data.pop("product")

    response = client.post(
        f"{API_version_string}products/{product.id}/updates/",
        headers=headers,
        json=data,
    )
    assert response.status_code == 200
