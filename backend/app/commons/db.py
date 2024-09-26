from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CommonMixin:
    """define a series of common elements that may be applied to mapped
    classes using this class as a mixin class."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    def __repr__(self):
        attrs = ", ".join(
            f"{key}={repr(value)}"
            for key, value in vars(self).items()
            if not key.startswith("_")
        )
        return f"{type(self).__name__}({attrs})"


class CreatedAt:
    created_at: Mapped[datetime] = mapped_column(insert_default=datetime.now())


class UpdatedAt:
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(), onupdate=func.current_timestamp()
    )
