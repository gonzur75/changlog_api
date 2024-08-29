from sqlalchemy.orm import Session

from app import models
from app.handlers.product import (
    create_product,
    delete_product,
    get_product_by_id,
    get_product_by_name,
)
from app.schemas import ProductCreate


def test_delete_product(session: Session, product_factory, user_factory) -> None:
    user = user_factory()
    product = product_factory(owner=user)

    assert get_product_by_name(session, name=product.name)

    delete_product(session=session, product_id=product.id, owner_id=user.id)
    product_db = get_product_by_id(session, product_id=product.id)

    assert product_db is None


def test_create_product(session: Session, user_factory) -> None:
    user = user_factory()
    db_user = (
        session.query(models.User).filter(models.User.username == user.username).first()
    )
    product = ProductCreate(name="Product1", owner_id=db_user.id)
    db_product = create_product(session, product)

    assert db_product
    assert db_product.name == product.name
