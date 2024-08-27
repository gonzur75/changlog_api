from datetime import datetime
from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session

from app import models
from app.main import app, get_db
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    test_json = {"username": "johndoe", "password": "password123"}
    response = client.post("/users/", json=test_json)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "created_at" and "id" in data
    assert test_json["username"] == data["username"]
    # user_id = data["id"]


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime


def get_user_by_name(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def hash_password(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)


def create_user(db, user):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/users/", response_model=User)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")

    return create_user(db, user)
