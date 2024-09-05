from polyfactory import Ignore, Use
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app import enums
from app.models import UpdatePoint, fake, Update, Product, User
from app.modules.auth import hash_password


class UpdatePointFactory(SQLAlchemyFactory[UpdatePoint]):
    id = Ignore()
    created_at = Ignore()
    updated_at = Ignore()
    name = Use(fake.text, max_nb_chars=50)
    body = Use(fake.text, max_nb_chars=255)
    status = Use(SQLAlchemyFactory.__random__.choice, list(enums.UpdatePointType))


class UpdateFactory(SQLAlchemyFactory[Update]):
    id = Ignore()
    created_at = Ignore()
    updated_at = Ignore()
    title = Use(fake.bothify, text="Update Number: #####")
    body = Use(fake.text, max_nb_chars=50)
    status = Use(SQLAlchemyFactory.__random__.choice, list(enums.UpdateStatus))
    version = Use(fake.bothify, text="#.#.#")


class ProductFactory(SQLAlchemyFactory[Product]):
    id = Ignore()
    created_at = Ignore()
    name = Use(fake.bothify, text="Update  Number: #####")


class UserFactory(SQLAlchemyFactory[User]):
    id = Ignore()
    hashed_password = Use(hash_password, password="secret123")
