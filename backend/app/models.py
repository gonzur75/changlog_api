import uuid
from typing import Optional


from app import enums
from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.commons.db import Base, CommonMixin, CreatedAt, UpdatedAt


class User(CommonMixin, CreatedAt, Base):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        back_populates="owner", cascade="all, delete"
    )


class Product(CreatedAt, CommonMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="products")
    updates: Mapped[list["Update"]] = relationship(
        back_populates="product", cascade="all, delete"
    )


class Update(CreatedAt, UpdatedAt, CommonMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    body: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[enums.UpdateStatus]
    version: Mapped[str] = mapped_column(String(50))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product: Mapped["Product"] = relationship(back_populates="updates")
    points: Mapped[list["UpdatePoint"]] = relationship(
        back_populates="update", cascade="all, delete"
    )


class UpdatePoint(CreatedAt, UpdatedAt, CommonMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    update_id: Mapped[int] = mapped_column(ForeignKey("updates.id"))
    type: Mapped[enums.UpdatePointType]
    update: Mapped["Update"] = relationship(back_populates="points")
