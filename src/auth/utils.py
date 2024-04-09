import datetime
from datetime import timedelta

from jose import JWTError, jwt

from settings import settings


def create_access_token(
    data: dict, expires_delta: timedelta | None = timedelta(minutes=15)
) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm
    )
    return encoded_jwt


def get_tokens(username: str) -> tuple[str, str]:
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=settings.auth.access_token_expires_minutes),
    )
    refresh_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=settings.auth.refresh_token_expires_minutes),
    )
    return (access_token, refresh_token)
