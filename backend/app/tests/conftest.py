from typing import Generator

import factory.alchemy
import pytest
from app import models, schemas
from app.api.dependencies import get_db
from app.enums import UpdatePointType, UpdateStatus
from app.handlers import create_user
from app.main import app
from app.models import Base
from app.modules.auth import hash_password
from faker import Faker
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

fake = Faker()


@pytest.fixture(name="session")
def session_db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def fake_db_user(session: Session):
    user = schemas.UserCreate(username=fake.user_name(), password=fake.password())
    db_user = create_user(session, user)
    yield db_user


@pytest.fixture
def fake_product(fake_db_user):
    yield models.Product(name="product_1", owner_id=fake_db_user.id)


@pytest.fixture
def user_factory(session):
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = models.User
            sqlalchemy_session = session
            sqlalchemy_session_persistence = "commit"

        username = factory.Sequence(lambda n: "User %d" % n)
        hashed_password = hash_password("secret123")

    return UserFactory


@pytest.fixture
def product_factory(session, user_factory):
    class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = models.Product
            sqlalchemy_session = session
            sqlalchemy_session_persistence = "commit"

        name = factory.Sequence(lambda n: "Product %d" % n)
        owner = factory.SubFactory(user_factory)

    return ProductFactory


class UpdateFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Update
        sqlalchemy_session_persistence = "commit"

    title = factory.Sequence(lambda n: "Product update %d" % n)
    body = fake.text(max_nb_chars=255)
    status = factory.Iterator(UpdateStatus)
    version = factory.Sequence(lambda n: "0.0.%d" % n)
    # product = factory.SubFactory(product_factory)


@pytest.fixture
def update_factory(session, product_factory):
    UpdateFactory._meta.sqlalchemy_session = session

    return UpdateFactory


class UpdatePointFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.UpdatePoint
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: "Update point %d" % n)
    description = fake.text(max_nb_chars=255)
    type = factory.Iterator(UpdatePointType)

    update = factory.SubFactory(UpdateFactory)
    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     async def create_coro(*args, **kwargs):
    #         return await model_class.create(*args, **kwargs)
    #
    #     return create_coro(*args, **kwargs)


@pytest.fixture
def update_point_factory(session, update_factory):
    UpdatePointFactory._meta.sqlalchemy_session = session

    return UpdatePointFactory
