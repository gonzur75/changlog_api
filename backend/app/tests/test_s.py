import app.enums
import factory
from app import models, schemas
from app.modules.config import API_version_string
from app.tests.utils import get_test_auth_header_and_user
from sqlalchemy.orm import Session
from starlette.testclient import TestClient


def test_delete_point(
    client: TestClient,
    user_factory,
    product_factory,
    update_factory,
    update_point_factory,
    session: Session,
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory(owner=user)
    update = update_factory(product=product)
    update_point = update_point_factory(update=update)

    response = client.delete(
        f"{API_version_string}points/{update_point.id}", headers=headers
    )
    assert response.status_code == 200
    assert "Point deleted successfully" in response.text
    check = (
        session.query(models.UpdatePoint)
        .filter(models.UpdatePoint.id == update.id)
        .first()
    )
    assert check is None


def test_patch_point(
    client: TestClient,
    user_factory,
    product_factory,
    update_factory,
    update_point_factory,
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory(owner=user)
    update = update_factory(product=product)
    update_point = update_point_factory(update=update)
    json = {"name": "Dark Mode", "type": app.enums.UpdatePointType.FIXED.value}

    response = client.patch(
        f"{API_version_string}points/{update_point.id}", headers=headers, json=json
    )
    assert response.status_code == 200
    print(response.request)
    assert json["name"] in response.json()["name"]
    assert update_point.type == app.enums.UpdatePointType.FIXED.value


def test_retrieve_point(
    client: TestClient,
    user_factory,
    product_factory,
    update_factory,
    update_point_factory,
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory(owner=user)
    update = update_factory(product=product)
    update_point = update_point_factory(update=update)

    response = client.get(
        f"{API_version_string}points/{update_point.id}", headers=headers
    )
    assert response.status_code == 200
    content = response.json()
    assert update_point.name == content["name"]


def test_add_update_point(
    client: TestClient,
    user_factory,
    product_factory,
    update_factory,
    update_point_factory,
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory(owner=user)
    update = update_factory(product=product)
    json = factory.build(dict, FACTORY_CLASS=update_point_factory)
    json.pop("update")

    response = client.post(
        f"{API_version_string}updates/{update.id}/points/", headers=headers, json=json
    )

    assert response.status_code == 200
    content = response.json()
    assert content["name"] == json["name"]


def test_get_product_updates(
    client: TestClient, user_factory, product_factory, update_factory
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory(owner=user)
    update_factory.create_batch(10, product=product)
    response = client.get(
        f"{API_version_string}products/{product.id}/updates/",
        headers=headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 10


def test_delete_update(
    client: TestClient, session: Session, user_factory, product_factory, update_factory
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory(owner=user)
    update = update_factory(product=product)
    response = client.delete(
        f"{API_version_string}updates/{update.id}", headers=headers
    )
    assert response.status_code == 200
    check = session.query(models.Update).filter(models.Update.id == update.id).first()
    assert check is None


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
