from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app import models


class ProductBase(BaseModel):
    name: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: UUID
    created_at: datetime


class Products(BaseModel):
    data: list[Product]


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


class UpdatePointBase(BaseModel):
    name: str
    description: str | None = None
    point_type: str


class UpdatePointCreate(UpdatePointBase):
    pass


class UpdatePoint(UpdatePointBase):
    created_at: datetime
    updated_at: datetime


class UpdateBase(BaseModel):
    title: str
    body: str | None = None
    status: models.UpdateStatus
    version: str


class UpdateCreate(UpdateBase):
    pass


class Update(UpdateBase):
    created_at: datetime
    updated_at: datetime
    product: Product
    points: list[UpdatePoint]
