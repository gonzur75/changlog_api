from pydantic import Field
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app import models, enums


class ProductBase(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]


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


class UpdateBase(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=50)]
    body: Annotated[str | None, Field(max_length=255)] = None
    status: models.UpdateStatus
    version: Annotated[str, Field(max_length=50)]


class UpdateCreate(UpdateBase):
    pass


class UpdatePatch(BaseModel):
    title: str | None = None
    body: str | None = None
    status: models.UpdateStatus | None = None
    version: str | None = None


class Update(UpdateBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    product: Product
    points: list["UpdatePoint"]


update_points_name = Field(
    min_length=3, max_length=50, examples=[enums.PointExample.name]
)
update_point_description = Field(
    max_length=255, examples=[enums.PointExample.description]
)


class UpdatePointBase(BaseModel):
    name: Annotated[str, update_points_name]
    description: Annotated[str | None, update_point_description]
    type: models.UpdatePointType


class UpdatePointPatch(BaseModel):
    name: Annotated[str | None, update_points_name]
    description: Annotated[str | None, update_point_description]
    type: models.UpdatePointType | None


class UpdatePointCreate(UpdatePointBase):
    pass


class UpdatePoint(UpdatePointBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    update_id: int


class Message(BaseModel):
    message: Annotated[str, Field(examples=["Success"])]
