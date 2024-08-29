from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: UUID
    created_at: datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    created_at: datetime
    id: UUID


class User(UserPublic):
    model_config = ConfigDict(from_attributes=True)

    products: list[Product] = []


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
