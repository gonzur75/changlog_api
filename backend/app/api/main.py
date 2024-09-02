from app.api.routes import point, product, signin, update, user
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user.router)
api_router.include_router(signin.router)
api_router.include_router(product.router)
api_router.include_router(update.router)
api_router.include_router(point.router)
