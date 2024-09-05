from typing import Annotated


from app import models, schemas
from app.api.dependencies import ProductCheckedDep, SessionDep
from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/", summary="List of updates for product")
async def product_updates(
    session: SessionDep,
    product: ProductCheckedDep,
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=0, le=100)] = 10,
) -> schemas.Updates:
    """
    List of updates for product
    """

    offset = (page - 1) * page
    limit = per_page * page
    query = (
        session.query(models.Update)
        .filter(models.Update.product_id == product.id)
        .order_by(models.Update.created_at)
    )
    paginated_query = query.offset(offset).limit(limit).all()
    return schemas.Updates(
        total=query.count(), page=page, size=per_page, data=paginated_query
    )


@router.post("/", summary="Create update for product")
async def create_update(
    session: SessionDep, update: schemas.UpdateCreate, product: ProductCheckedDep
) -> schemas.Update:
    """
    Create update for product wth:
    - **title**: update title
    - **body**: some more info about update
    - **status**: update status (in_progress, in_review etc.)
    - **version**: product version
    """
    db_update = models.Update(**update.model_dump(), product_id=product.id)
    session.add(db_update)
    session.commit()
    session.refresh(db_update)
    return db_update
