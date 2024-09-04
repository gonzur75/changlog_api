from polyfactory import Ignore, Use
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app import enums
from app.models import UpdatePoint, fake, Update, Product, User
from app.modules.auth import hash_password


class UpdatePointPolyFactory(SQLAlchemyFactory[UpdatePoint]):
    __set_relationships__ = True
    id = Ignore()
    created_at = Ignore()
    updated_at = Ignore()
    name = Use(fake.text, max_nb_chars=50)
    body = Use(fake.text, max_nb_chars=255)
    status = Use(SQLAlchemyFactory.__random__.choice, list(enums.UpdatePointType))


class UpdatePolyFactory(SQLAlchemyFactory[Update]):
    __set_relationships__ = True

    id = Ignore()
    created_at = Ignore()
    updated_at = Ignore()
    title = Use(fake.bothify, text="Update Number: #####")
    body = Use(fake.text, max_nb_chars=50)
    status = Use(SQLAlchemyFactory.__random__.choice, list(enums.UpdateStatus))
    version = Use(fake.bothify, text="#.#.#")
    points = Use(UpdatePointPolyFactory.batch, size=12)


class ProductPolyFactory(SQLAlchemyFactory[Product]):
    id = Ignore()
    created_at = Ignore()
    name = Use(fake.bothify, text="Update  Number: #####")


class UserPolyFactory(SQLAlchemyFactory[User]):
    id = Ignore()
    hashed_password = Use(hash_password, password="secret123")
