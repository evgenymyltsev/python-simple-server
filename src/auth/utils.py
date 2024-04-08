import datetime
from datetime import timedelta
from typing import Optional

from jose import JWTError, jwt

from config import (
    ACCESS_TOKEN_EXPIRES_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRES_MINUTES,
    SECRET_KEY,
)


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=15)
) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_tokens(username: str) -> tuple[str, str]:
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES),
    )
    refresh_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES),
    )
    return (access_token, refresh_token)
