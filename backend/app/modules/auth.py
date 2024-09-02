from datetime import datetime, timedelta

import bcrypt
import jwt
from app.modules.config import settings
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_version_string}signin")


def hash_password(password) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt).decode()


def create_jwt_token(username):
    expire_delta = ACCESS_TOKEN_EXPIRE_MINUTES if not None else 15
    expire = datetime.now() + timedelta(minutes=expire_delta)
    data = {"sub": username, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_username_from_jwt(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")


def compare_password(password, hashed_password) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def authenticate_user(db, username, password):
    from app.handlers.user import get_user_by_username

    user_db = get_user_by_username(db, username)
    if not user_db:
        return None
    if not compare_password(password=password, hashed_password=user_db.hashed_password):
        return None
    return user_db
