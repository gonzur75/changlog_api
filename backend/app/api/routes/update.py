from fastapi import APIRouter

from app import schemas, models, enums
from app.api.dependencies import UpdateCheckedDep, SessionDep
from app.api.routes import update_points


router = APIRouter(prefix="/updates", tags=[enums.RouterTags.update])
router.include_router(update_points.router)


@router.get("/{update_id}", summary="Retrieve update")
async def retrieve_update(update: UpdateCheckedDep) -> schemas.UpdatePoints:
    """Retrieve a update"""

    return update


@router.patch("/{update_id}", summary="Modify update data")
async def patch_update(
    session: SessionDep, stored_update: UpdateCheckedDep, update_in: schemas.UpdatePatch
) -> schemas.Update:
    """
    Modify update (all fields are optional) with:
    - **title**: update title
    - **body**: some more info about update
    - **status**: update status (in_progress, in_review etc)
    - **version**: version
    """

    update_data = update_in.model_dump(exclude_unset=True)
    update_query = session.query(models.Update).filter(
        models.Update.id == stored_update.id
    )
    update_query.update(update_data, synchronize_session=False)
    session.commit()
    session.refresh(stored_update)
    return stored_update


@router.delete("/{update_id}", summary="Delete update")
async def delete_update(
    session: SessionDep,
    update: UpdateCheckedDep,
) -> schemas.Message:
    """Delete point"""
    session.delete(update)
    session.commit()
    return schemas.Message(message="Update deleted successfully")
