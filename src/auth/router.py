import json

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from config import ALGORITHM, SECRET_KEY
from src.auth.schemas import RefreshToken, Token
from src.auth.service import AuthService
from src.auth.utils import get_tokens
from src.cache import Cache
from src.error import InternalServerError
from src.users.schemas import SUser

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        print("form_data > ", form_data)
        user = await AuthService.get_user(form_data.username, form_data.password)
        if Cache.get(form_data.username):
            print("user from cache > ", Cache.get(form_data.username))
            user = SUser.model_validate(json.loads(Cache.get(form_data.username)))
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
            print("user from db > ", user.model_dump(), type(user))
            Cache.set(form_data.username, user.model_dump_json())
        (access_token, refresh_token) = get_tokens(user.username)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise InternalServerError(e)


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: RefreshToken):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    (access_token, refresh_token) = get_tokens(username)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
