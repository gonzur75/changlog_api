from typing import Any

from fastapi import APIRouter, HTTPException
from starlette import status

from app import schemas, handlers
from app.api.dependencies import SessionDep, CurrentUser
from app.handlers.product import get_product_by_id

router = APIRouter()
not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
)
not_your_product_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Not your product"
)


@router.patch("/{product_id}")
async def change_product_name(
    session: SessionDep,
    product_id,
    product: schemas.ProductBase,
    current_user: CurrentUser,
):
    db_product = handlers.get_product_by_id(session, product_id)
    if not db_product:
        raise not_found_exception
    if db_product.owner_id != current_user.id:
        raise not_your_product_exception
    db_product.name = product.name
    session.commit()
    session.refresh(db_product)


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
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
        raise not_found_exception
    if product.owner_id != current_user.id:
        raise not_your_product_exception
    return product
