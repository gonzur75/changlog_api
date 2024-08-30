from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app import schemas, handlers
from app.api.dependencies import SessionDep, get_current_active_user
from app.handlers.product import get_product_by_id

router = APIRouter()


@router.post("/", response_model=schemas.Product)
async def create_product(
    session: SessionDep,
    product: schemas.ProductCreate,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return handlers.create_product(session, product, current_user.id)


@router.get("/{product_id}", response_model=schemas.Product)
async def retrieve_product(
    product_id: int,
    session: SessionDep,
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
) -> Any:
    product = get_product_by_id(session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not your product"
        )
    return product
