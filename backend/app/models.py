import uuid
from datetime import datetime

from sqlalchemy import func, String, Uuid
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, declared_attr


class Base(DeclarativeBase):
    pass


class CommonMixin:
    """define a series of common elements that may be applied to mapped
    classes using this class as a mixin class."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class CreatedAt:
    created_at: Mapped[datetime] = mapped_column(insert_default=datetime.now())


class UpdatedAt:
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now)


class User(CreatedAt, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4())
    username: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
