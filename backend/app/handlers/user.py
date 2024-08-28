from app import models
from app.modules.auth import hash_password


def get_user_by_name(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db, user):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
