from sqlalchemy.orm import Session
from starlette.testclient import TestClient

import app.enums
from app import models
from app.modules.config import settings
from app.tests.utils import get_test_auth_header_and_user


def test_delete_point(
    client: TestClient,
    user_factory,
    product_factory,
    update_factory,
    update_point_factory,
    session: Session,
):
    headers, user = get_test_auth_header_and_user(user_factory)
    product = product_factory.create_sync(owner=user)
    update = update_factory.create_sync(product=product)
    update_point = update_point_factory.create_sync(update=update)

    response = client.delete(
        f"{settings.API_version_string}points/{update_point.id}", headers=headers
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
    product = product_factory.create_sync(owner=user)
    update = update_factory.create_sync(product=product)
    update_point = update_point_factory.create_sync(update=update)
    json = {"name": "Dark Mode", "type": app.enums.UpdatePointType.FIXED.value}

    response = client.patch(
        f"{settings.API_version_string}points/{update_point.id}",
        headers=headers,
        json=json,
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
    product = product_factory.create_sync(owner=user)
    update = update_factory.create_sync(product=product)
    update_point = update_point_factory.create_sync(update=update)

    response = client.get(
        f"{settings.API_version_string}points/{update_point.id}", headers=headers
    )
    assert response.status_code == 200
    content = response.json()
    assert update_point.name == content["name"]
