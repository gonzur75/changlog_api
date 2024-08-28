import os
from datetime import datetime, timedelta

import bcrypt
import jwt

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)


def create_jwt_token(username):
    expire_delta = ACCESS_TOKEN_EXPIRE_MINUTES if not None else 15
    expire = datetime.now() + timedelta(expire_delta)
    data = {"sub": username, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def compare_password(password, hashed_password) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def authenticate_user(db, username, password):
    from app.handlers.user import get_user_by_name

    user_db = get_user_by_name(db, username)
    if not user_db:
        return None
    if not compare_password(password, user_db.hashed_password):
        return None
    return user_db
