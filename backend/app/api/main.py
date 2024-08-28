from fastapi import APIRouter

from app.api.routes import user
from app.api.routes.signin import router

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users")
api_router.include_router(router, prefix="/signin")
