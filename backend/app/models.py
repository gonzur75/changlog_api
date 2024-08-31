import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, String, Uuid, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class UpdateStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    SHIPPED = "shipped"
    DEPRECATED = "deprecated"


class UpdatePointType(str, Enum):
    NEW = "new"
    IMPROVED = "improved"
    FIXED = "fixed"
    UPDATED = "updated"
    DEPRECATED = "deprecated"
    REMOVED = "removed"


class Base(DeclarativeBase):
    pass


class CommonMixin:
    """define a series of common elements that may be applied to mapped
    classes using this class as a mixin class."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    id: Mapped[int] = mapped_column(primary_key=True)


class CreatedAt:
    created_at: Mapped[datetime] = mapped_column(insert_default=datetime.now())


class UpdatedAt:
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(), onupdate=func.current_timestamp()
    )


class User(CreatedAt, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        back_populates="owner", cascade="all, delete"
    )


class Product(CreatedAt, CommonMixin, Base):
    name: Mapped[str] = mapped_column(String(50))
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="products")
    updates: Mapped[list["Update"]] = relationship(
        back_populates="product", cascade="all, delete"
    )


class Update(CreatedAt, UpdatedAt, CommonMixin, Base):
    title: Mapped[str] = mapped_column(String(50))
    body: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[UpdateStatus]
    version: Mapped[str] = mapped_column(String(50))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product: Mapped["Product"] = relationship(back_populates="updates")
    points: Mapped[list["UpdatePoint"]] = relationship(
        back_populates="update", cascade="all, delete"
    )


class UpdatePoint(CreatedAt, UpdatedAt, CommonMixin, Base):
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    update_id: Mapped[int] = mapped_column(ForeignKey("updates.id"))
    point_type: Mapped[UpdatePointType]
    update: Mapped["Update"] = relationship(back_populates="points")
