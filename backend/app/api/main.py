from fastapi import APIRouter

from app.api.routes import user, signin, product, update, point

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users")
api_router.include_router(signin.router, prefix="/signin")
api_router.include_router(product.router, prefix="/products")
api_router.include_router(update.router, prefix="/updates")
api_router.include_router(point.router, prefix="/points")
