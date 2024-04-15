import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from logger import get_logger
from settings import settings
from src.auth.schemas import SRefreshToken, SToken
from src.auth.service import AuthService
from src.auth.utils import get_tokens
from src.cache import Cache
from src.error import InternalServerError
from src.users.schemas import SUser

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=SToken)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    try:
        user_from_cache = Cache.get(form_data.username)
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
        (access_token, refresh_token) = get_tokens(user.username)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError


@router.post("/refresh", response_model=SToken)
async def refresh_token(refresh_token: SRefreshToken) -> SToken:
    payload = jwt.decode(refresh_token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
    username = payload.get("sub")

    return get_tokens(username)
