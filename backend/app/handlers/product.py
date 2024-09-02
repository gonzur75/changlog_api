from uuid import UUID

from app import models, schemas
from sqlalchemy.orm import Session


def create_product(session: Session, product: schemas.ProductCreate, user_id: UUID):
    db_product = models.Product(**product.model_dump(), owner_id=user_id)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def get_product_by_id(session: Session, product_id: int):
    return session.query(models.Product).filter(models.Product.id == product_id).first()


def delete_product(session, product_id: int, owner_id: UUID):
    session.query(models.Product).filter(models.Product.id == product_id).filter(
        models.Product.owner_id == owner_id
    ).delete()
    session.commit()


def get_product_by_name(session, name):
    return session.query(models.Product).filter(models.Product.name == name).first()


def get_products_for_user(session: Session, user_id: UUID):
    return (
        session.query(models.Product).filter(models.Product.owner_id == user_id).all()
    )
