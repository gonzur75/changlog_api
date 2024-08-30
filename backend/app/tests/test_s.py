import factory
from starlette.testclient import TestClient

from app.main import API_version_string
from app.tests.utils import get_test_auth_header_and_user


def test_create_update_endpoint(
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
