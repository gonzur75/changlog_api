from typing import Generator

import pytest

from app import factories
from app.api.dependencies import get_db
from app.main import app
from app.models import Base
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
def user_factory(session):
    factories.UserFactory.__session__ = session

    return factories.UserFactory


@pytest.fixture
def product_factory(session, user_factory):
    factories.ProductFactory.__session__ = session

    return factories.ProductFactory


@pytest.fixture
def update_factory(session, product_factory):
    factories.UpdateFactory.__session__ = session

    return factories.UpdateFactory


@pytest.fixture
def update_point_factory(session, update_factory):
    factories.UpdatePointFactory.__session__ = session

    return factories.UpdatePointFactory
