from fastapi import APIRouter, HTTPException

from app import handlers, schemas
from app.api.dependencies import SessionDep

from app.handlers.user import get_user_by_username

router = APIRouter()


@router.post("/", response_model=schemas.UserPublic)
def create_user(
    user: schemas.UserCreate,
    db: SessionDep,
):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")

    return handlers.create_user(db, user)


async def root():
    return {"message": "Hi I'm Changelog nice to meet you"}
