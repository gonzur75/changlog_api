from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import models, schemas, factories
from app.modules.config import settings
from app.tests.utils import get_test_auth_header_and_user


def test_delete_update(
    client: TestClient, session: Session, user_factory, product_factory, update_factory
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory.create_sync(owner=user)
    update = update_factory.create_sync(product=product)
    response = client.delete(
        f"{settings.API_version_string}updates/{update.id}", headers=headers
    )
    assert response.status_code == 200
    check = session.query(models.Update).filter(models.Update.id == update.id).first()
    assert check is None


def test_modify_update(
    client: TestClient, user_factory, product_factory, update_factory
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory.create_sync(owner=user)
    update = update_factory.create_sync(product=product)

    json = {"title": "New Title"}
    response = client.patch(
        f"{settings.API_version_string}updates/{update.id}", headers=headers, json=json
    )
    assert response.status_code == 200
    content = schemas.Update(**response.json())
    assert content.title == json["title"]
    assert content.updated_at != content.created_at


def test_retrieve_update(
    client: TestClient, user_factory, update_factory, product_factory
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory.create_sync(owner=user)
    update = update_factory.create_sync(product=product)

    response = client.get(
        f"{settings.API_version_string}updates/{update.id}", headers=headers
    )
    print(response.text)
    assert response.status_code == 200
    content = schemas.Update(**response.json())
    assert content.id == update.id


def test_create_update(
    client: TestClient, user_factory, update_factory, product_factory
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory.create_sync(owner=user)

    data = factories.UpdateFactory.process_kwargs()

    response = client.post(
        f"{settings.API_version_string}products/{product.id}/updates/",
        headers=headers,
        json=data,
    )
    assert response.status_code == 200


def test_add_update_point(
    client: TestClient,
    user_factory,
    product_factory,
    update_factory,
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory.create_sync(owner=user)
    update = update_factory.create_sync(product=product)
    data = factories.UpdatePointFactory.process_kwargs()

    response = client.post(
        f"{settings.API_version_string}updates/{update.id}/points/",
        headers=headers,
        json=data,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
