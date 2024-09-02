from app import models
from sqlalchemy.orm import Session


def get_update_by_id(session: Session, update_id: int):
    return session.query(models.Update).filter(models.Update.id == update_id).first()
