from fastapi import APIRouter

from app import schemas, models
from app.api.dependencies import PointCheckedDep, SessionDep

router = APIRouter()


@router.delete("/{point_id}")
async def delete_point(
    stored_point: PointCheckedDep,
    session: SessionDep,
) -> schemas.Message:
    session.delete(stored_point)
    session.commit()
    return schemas.Message(message="Item deleted successfully")


@router.patch("/{point_id}", response_model=schemas.SingleUpdatePoint)
async def update_point(
    stored_point: PointCheckedDep,
    session: SessionDep,
    point_in: schemas.UpdatePointPatch,
):
    update_data = point_in.model_dump(exclude_unset=True)
    update_query = session.query(models.UpdatePoint).filter(
        models.UpdatePoint.id == stored_point.id
    )
    update_query.update(update_data, synchronize_session=False)
    session.commit()
    session.refresh(stored_point)
    return stored_point


@router.get("/{point_id}", response_model=schemas.SingleUpdatePoint)
async def retrieve_point(point: PointCheckedDep):
    return point
