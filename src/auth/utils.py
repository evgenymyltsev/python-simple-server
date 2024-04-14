import datetime
from datetime import timedelta

from jose import jwt

from settings import settings
from src.auth.schemas import SToken


def create_access_token(data: dict, expires_delta: timedelta | None = timedelta(minutes=20)) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)
    return encoded_jwt


def get_tokens(username: str) -> SToken:
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=settings.auth.access_token_expires_minutes),
    )
    refresh_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=settings.auth.refresh_token_expires_minutes),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
