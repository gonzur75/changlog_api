from fastapi import HTTPException, APIRouter

from app.api.dependencies import SessionDep

from app.schemas import User, UserCreate
from app import handlers

router = APIRouter()


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: SessionDep):
    db_user = handlers.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")

    return handlers.create_user(db, user)


async def root():
    return {"message": "Hi I'm Changelog nice to meet you"}
