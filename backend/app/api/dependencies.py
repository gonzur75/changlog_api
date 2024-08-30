from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette import status

from app import schemas
from app.db import engine
from app.handlers.user import get_user_by_username
from app.modules.auth import get_username_from_jwt


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


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
