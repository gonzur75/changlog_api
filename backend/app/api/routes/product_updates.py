from fastapi import APIRouter

from app import schemas, models
from app.api.dependencies import SessionDep, ProductCheckedDep

router = APIRouter()


@router.get("/")
async def product_updates(product: ProductCheckedDep) -> schemas.Updates:
    return product.updates


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
