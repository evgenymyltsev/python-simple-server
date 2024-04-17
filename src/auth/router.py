"""Authentication API Router.

This module contains the FastAPI API router for authentication endpoints.

Attributes:
    router (APIRouter): The APIRouter instance for authentication.

"""

import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from logger import get_logger
from src.auth.schemas import SRefreshToken, SToken
from src.auth.service import AuthService
from src.auth.utils import get_tokens, jwt_decode
from src.cache import Cache
from src.error import InternalServerError
from src.users.schemas import SUser
from src.users.service import UserService

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=SToken)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    """Authenticate a user and returns an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The request form containing the
            username and password.

    Returns:
        dict[str, str]: A dictionary containing the access token, refresh token,
            and token type.

    Raises:
        HTTPException: If the username or password is incorrect.

    """
    try:
        user_from_cache = Cache.get(form_data.username)
        logger.debug(form_data.username, form_data.password)
        if user_from_cache:
            logger.debug(f"user from cache > {user_from_cache}")
            user = SUser.model_validate(json.loads(user_from_cache))
        else:
            user = await AuthService.get_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "data": None,
                        "detail": "Incorrect username or password",
                    },
                    headers={"WWW-Authenticate": "Bearer"},
                )
            logger.debug(f"user from db > {user}")
            Cache.set(form_data.username, user.model_dump_json())
        return get_tokens(user.username)
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError


@router.post("/refresh", response_model=SToken)
async def refresh_token(refresh_token: SRefreshToken) -> SToken:
    """Refresh a token using a refresh token.

    Args:
        refresh_token (SToken): The refresh token to be refreshed.

    Returns:
        SToken: A new token with a new access and refresh token.

    Raises:
        HTTPException: If the refresh token is invalid or expired.

    """
    payload = jwt_decode(refresh_token)
    username = payload.get("sub")

    return get_tokens(username)


@router.get("/verify-email/")
async def verify_email(token: str) -> SUser | None:
    """Verify an email using a token.

    Args:
        token (str): The token to verify the email.

    Returns:
        SUser or None: The verified user, or None if the token is invalid.

    Raises:
        HTTPException: If the token is expired.

    """
    try:
        payload = jwt_decode(token)
        user_email = payload.get("email")
        if not user_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        user = await UserService.update_email_verified(user_email, True)
        return user
    except jwt.ExpiredSignatureError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Signature expired")
    except jwt.JWTError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    except Exception as e:
        logger.error(e)
        raise InternalServerError
