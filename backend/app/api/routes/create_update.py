from fastapi import APIRouter

from app import schemas, models
from app.api.dependencies import SessionDep, ProductChecked

router = APIRouter()


@router.post("/", response_model=schemas.Update)
async def create_update(
    session: SessionDep, update: schemas.UpdateCreate, product: ProductChecked
):
    db_update = models.Update(**update.model_dump(), product_id=product.id)
    session.add(db_update)
    session.commit()
    session.refresh(db_update)
    return db_update
