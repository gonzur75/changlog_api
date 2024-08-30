from typing import Any

from fastapi import APIRouter, HTTPException
from starlette import status

from app import schemas, handlers
from app.api.dependencies import SessionDep, CurrentUser
from app.handlers.product import get_product_by_id

router = APIRouter()


@router.post("/", response_model=schemas.Product)
async def create_product(
    session: SessionDep,
    product: schemas.ProductCreate,
    current_user: CurrentUser,
):
    return handlers.create_product(session, product, current_user.id)


@router.get("/", response_model=schemas.Products)
async def retrieve_products(session: SessionDep, current_user: CurrentUser):
    data = handlers.get_products_for_user(session, user_id=current_user.id)

    return schemas.Products(data=data)


@router.get("/{product_id}", response_model=schemas.Product)
async def retrieve_product(
    product_id: int,
    session: SessionDep,
    current_user: CurrentUser,
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
