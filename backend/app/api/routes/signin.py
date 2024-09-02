from typing import Annotated

from app import enums
from app.api.dependencies import SessionDep
from app.modules.auth import authenticate_user, create_jwt_token
from app.schemas import Token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

router = APIRouter(prefix="/signin", tags=[enums.RouterTags.users])


@router.post("/")
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt_token(username=user.username)

    return Token(access_token=access_token, token_type="bearer")
