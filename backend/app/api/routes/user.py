from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas import User, UserCreate
from app import handlers

router = APIRouter()


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = handlers.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")

    return handlers.create_user(db, user)


@router.get("/")
async def root():
    return {"message": "Hi I'm Changelog nice to meet you"}
