"""
Utility functions for handling JWT tokens.

This module provides functions for encoding and decoding JWT tokens, as well as
utilities for verifying and manipulating tokens.

"""

import datetime
from datetime import timedelta

from jose import jwt

from settings import settings
from src.schemas.auth import SToken


def jwt_decode(token: str) -> dict:
    """Decode a JWT token and return its payload as a dictionary.

    Args:
        token (str): The JWT token to be decoded.

    Returns:
        dict: The payload of the JWT token.

    Raises:
        jose.jwt.ExpiredSignatureError: If the token has expired.
        jose.jwt.JWTError: If the token is invalid.
    """
    return jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])


def jwt_encode(data: dict) -> str:
    """Encode a JWT token with the given data and return it as a string.

    Args:
        data (dict): The data to be encoded into the token.
        algorithm (str): The algorithm used to sign the token.

    Returns:
        str: The encoded JWT token.
    """
    return jwt.encode(data, settings.auth.secret_key, algorithm=settings.auth.algorithm)


def create_access_token(data: dict, expires_delta: timedelta | None = timedelta(minutes=20)) -> str:
    """Create a JWT access token with the given data and return it as a string.

    Args:
        data (dict): The data to be encoded into the token.
        expires_delta (datetime.timedelta, optional): The time until the token expires.
            Defaults to 20 minutes.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(data=to_encode)
    return encoded_jwt


def get_tokens(username: str) -> SToken:
    """Generate access and refresh tokens for the given username.

    Args:
        username (str): The username for which to generate tokens.

    Returns:
        SToken: A dictionary containing the access and refresh tokens.

    """
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
