from fastapi import APIRouter

from app import schemas, models
from app.api.dependencies import SessionDep, UpdateCheckedDep

router = APIRouter(prefix="/{update_id}/points")


@router.post("/", summary="Create point for update")
async def create_point_for_update(
    session: SessionDep, update: UpdateCheckedDep, point: schemas.UpdatePointCreate
) -> schemas.UpdatePoint:
    """
    Create point for update with:
    - **name**: point name
    - **description**: a long description
    - **type**: a typ of point
    """
    db_point = models.UpdatePoint(**point.model_dump(), update_id=update.id)
    session.add(db_point)
    session.commit()
    session.refresh(db_point)
    return db_point
