from fastapi import APIRouter
from starlette import status

from app import schemas, handlers, enums
from app.api.dependencies import (
    SessionDep,
    CurrentUser,
    ProductCheckedDep,
)
from app.api.routes import product_updates

router = APIRouter(prefix="/products", tags=[enums.RouterTags.product])

router.include_router(product_updates.router, prefix="/{product_id}/updates")


@router.post(
    "/", status_code=status.HTTP_201_CREATED, summary="Create products for current user"
)
async def create_product(
    session: SessionDep,
    product: schemas.ProductCreate,
    current_user: CurrentUser,
) -> schemas.Product:
    """Create product with:
    - **name**: product name
    """
    return handlers.create_product(session, product, current_user.id)


@router.get("/", summary="Retrieve products for current user")
async def retrieve_products_for_current_user(
    session: SessionDep, current_user: CurrentUser
) -> schemas.Products:
    """Retrieve all products for current user"""
    data = handlers.get_products_for_user(session, user_id=current_user.id)

    return schemas.Products(data=data)


@router.get("/{product_id}", summary="Retrieve product")
async def retrieve_product(product: ProductCheckedDep) -> schemas.ProductUpdates:
    """Retrieve a product by id"""
    return product


@router.patch("/{product_id}", summary="Modify product name")
async def change_product_name(
    session: SessionDep,
    stored_product: ProductCheckedDep,
    product: schemas.ProductBase,
):
    """
    Modify product :
    - **name**: product name
    """
    stored_product.name = product.name
    session.commit()
    session.refresh(stored_product)


@router.delete("/{product_id}", summary="Delete product")
async def delete_point(
    stored_product: ProductCheckedDep,
    session: SessionDep,
) -> schemas.Message:
    """Delete product"""
    session.delete(stored_product)
    session.commit()
    return schemas.Message(message="Product deleted successfully")
