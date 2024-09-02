from app import handlers
from app.schemas import UserCreate
from app.tests.conftest import fake
from sqlalchemy.orm import Session


def test_create_user_in_db(session: Session) -> None:
    username = fake.user_name()
    password = fake.password()
    user_create = UserCreate(username=username, password=password)
    user = handlers.create_user(session, user_create)
    assert user.username == username
    assert hasattr(user, "hashed_password")
