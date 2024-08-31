from fastapi import APIRouter

from app import schemas, models
from app.api.dependencies import SessionDep, UpdateCheckedDep

router = APIRouter()


@router.get("/", response_model=list[schemas.UpdatePoint])
async def update_points(update: UpdateCheckedDep):
    return update.points


@router.post("/", response_model=schemas.UpdatePoint)
async def create_point(
    session: SessionDep, update: UpdateCheckedDep, point: schemas.UpdatePointCreate
):
    db_point = models.UpdatePoint(**point.model_dump(), update_id=update.id)
    session.add(db_point)
    session.commit()
    session.refresh(db_point)
    return db_point
