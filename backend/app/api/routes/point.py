from fastapi import APIRouter

from app import schemas, models, enums
from app.api.dependencies import PointCheckedDep, SessionDep


router = APIRouter(prefix="/points", tags=[enums.RouterTags.points])


@router.get("/{point_id}", summary="Retrieve point")
async def retrieve_point(point: PointCheckedDep) -> schemas.UpdatePoint:
    """Retrieve a point"""

    return point


@router.patch("/{point_id}", summary="Modify point data")
async def update_point(
    stored_point: PointCheckedDep,
    session: SessionDep,
    point_in: schemas.UpdatePointPatch,
) -> schemas.UpdatePoint:
    """
    Update point (all fields are optional) with:
    - **name**: point name
    - **description**: a long description
    - **type**: a typ of point
    """

    update_data = point_in.model_dump(exclude_unset=True)
    update_query = session.query(models.UpdatePoint).filter(
        models.UpdatePoint.id == stored_point.id
    )
    update_query.update(update_data, synchronize_session=False)
    session.commit()
    session.refresh(stored_point)
    return stored_point


@router.delete("/{point_id}", summary="Delete point")
async def delete_point(
    stored_point: PointCheckedDep,
    session: SessionDep,
) -> schemas.Message:
    """Delete point"""
    session.delete(stored_point)
    session.commit()
    return schemas.Message(message="Point deleted successfully")
