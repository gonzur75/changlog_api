from fastapi import APIRouter

from app import schemas, models
from app.api.dependencies import UpdateCheckedDep, SessionDep

router = APIRouter()


@router.delete("/{update_id}")
async def delete_update(
    session: SessionDep,
    update: UpdateCheckedDep,
):
    session.delete(update)
    session.commit()
    return {"message": "Success"}


@router.patch("/{update_id}", response_model=schemas.Update)
async def patch_update(
    session: SessionDep, stored_update: UpdateCheckedDep, update_in: schemas.UpdatePatch
):
    update_data = update_in.model_dump(exclude_unset=True)
    update_query = session.query(models.Update).filter(
        models.Update.id == stored_update.id
    )
    update_query.update(update_data, synchronize_session=False)
    session.commit()
    session.refresh(stored_update)
    return stored_update


@router.get("/{update_id}", response_model=schemas.Update)
async def retrieve_update(update: UpdateCheckedDep):
    return update
