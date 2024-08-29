from typing import Annotated

from fastapi import APIRouter, Depends

from app import schemas, handlers
from app.api.dependencies import SessionDep, get_current_active_user

router = APIRouter()


@router.post("/", response_model=schemas.Product)
async def create_product(
    session: SessionDep,
    product: schemas.ProductCreate,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return handlers.create_product(session, product, current_user.id)
