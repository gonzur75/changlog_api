from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, Path
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, handlers, models, enums
from app.db import engine
from app.handlers.user import get_user_by_username
from app.modules.auth import get_username_from_jwt, oauth2_scheme


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username: str = get_username_from_jwt(token)
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    return current_user


CurrentUser = Annotated[schemas.User, Depends(get_current_active_user)]


async def product_get(
    session: SessionDep, product_id: Annotated[int, Path(title="ID of update", ge=1)]
):
    db_product = handlers.get_product_by_id(session, product_id)
    return db_product


async def product_checked(
    db_product: Annotated[schemas.Product, Depends(product_get)],
    current_user: CurrentUser,
):
    if not db_product:
        raise not_found_exception
    if db_product.owner_id != current_user.id:
        raise not_your_product_exception
    return db_product


ProductCheckedDep = Annotated[schemas.Product, Depends(product_checked)]


def not_your_resource(resource_name):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"You have no access to {resource_name}",
    )


not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail=enums.ExceptionMessages.not_found
)
not_your_product_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Not your product"
)


async def get_update(
    session: SessionDep, update_id: Annotated[int, Path(title="ID of update", ge=1)]
):
    return handlers.get_update_by_id(session, update_id)


async def get_update_checked(
    update: Annotated[schemas.Update, Depends(get_update)], current_user: CurrentUser
):
    if not update:
        raise not_found_exception
    if update.product.owner_id != current_user.id:
        raise not_your_resource(update.title)
    return update


UpdateCheckedDep = Annotated[schemas.Update, Depends(get_update_checked)]


async def get_point(
    session: SessionDep,
    point_id: Annotated[int, Path(title="ID of update point", ge=1)],
):
    return (
        session.query(models.UpdatePoint)
        .filter(models.UpdatePoint.id == point_id)
        .first()
    )


async def get_point_checked(
    point: Annotated[schemas.UpdatePoint, Depends(get_point)], current_user: CurrentUser
):
    if not point:
        raise not_found_exception
    if point.update.product.owner_id != current_user.id:
        raise not_your_resource(point.name)

    return point


PointCheckedDep = Annotated[schemas.UpdatePoint, Depends(get_point_checked)]
