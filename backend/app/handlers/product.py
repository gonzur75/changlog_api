from sqlalchemy.orm import Session

from app import models, schemas
from app.schemas import Product


def create_product(db: Session, product: schemas.ProductCreate) -> schemas.Product:
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_id(session: Session, product_id: int) -> Product | None:
    return session.query(models.Product).filter(models.Product.id == product_id).first()


def delete_product(session, product_id, owner_id):
    session.query(models.Product).filter(models.Product.id == product_id).filter(
        models.Product.owner_id == owner_id
    ).delete()
    session.commit()


def get_product_by_name(session, name):
    return session.query(models.Product).filter(models.Product.name == name).first()
