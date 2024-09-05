from app import models
from app.handlers.product import (
    create_product,
    delete_product,
    get_product_by_id,
    get_product_by_name,
    get_products_for_user,
)
from app.schemas import ProductCreate
from sqlalchemy.orm import Session


def test_get_products_for_user(session: Session, user_factory, product_factory):
    user = user_factory.create_sync()
    product_factory.create_batch_sync(10, owner=user)

    db_products = get_products_for_user(session=session, user_id=user.id)

    assert db_products
    assert len(db_products) == 10
    assert db_products[5].owner_id == user.id


def test_delete_product(session: Session, product_factory, user_factory) -> None:
    user = user_factory.create_sync()
    product = product_factory.create_sync(owner=user)

    assert get_product_by_name(session, name=product.name)

    delete_product(session=session, product_id=product.id, owner_id=user.id)
    product_db = get_product_by_id(session, product_id=product.id)

    assert product_db is None


def test_create_product(session: Session, user_factory) -> None:
    user = user_factory.create_sync()
    db_user = (
        session.query(models.User).filter(models.User.username == user.username).first()
    )
    assert db_user

    product = ProductCreate(name="Product1")
    db_product = create_product(session, product, user_id=db_user.id)

    assert db_product
    assert db_product.name == product.name
