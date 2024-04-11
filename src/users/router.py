import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from src.error import InternalServerError
from src.users.models import Role
from src.users.schemas import SCreateUser, SUpdateUser, SUser
from src.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

http_forbidden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Only admin or current user can perform this action",
)


@router.post("", response_model=SUser)
async def create_user(
    body: SCreateUser,
) -> SUser:
    try:
        user = await UserService.add_user(data=body)
        return user
    except HTTPException as e:
        raise e
    except Exception:
        raise InternalServerError


@router.get("/{user_id}/", response_model=SUser)
async def get_user_by_id(
    user_id: uuid.UUID,
) -> SUser:
    try:
        user = await UserService.get_user_by_field(field="user_id", value=user_id)
        return user
    except HTTPException as e:
        raise e
    except Exception:
        raise InternalServerError


@router.get("", response_model=list[SUser])
async def get_all_users(
    current_user: SUser = Depends(UserService.get_current_user),
) -> list[SUser]:
    try:
        if current_user.role != Role.ADMIN:
            raise http_forbidden_error
        users = await UserService.get_all_users()
        return users
    except HTTPException as e:
        raise e
    except Exception:
        raise InternalServerError


@router.patch("/{user_id}/", response_model=SUser)
async def update_user(
    user_id: uuid.UUID,
    body: SUpdateUser,
    current_user: SUser = Depends(UserService.get_current_user),
) -> SUser:
    try:
        if current_user.role != Role.ADMIN and current_user.user_id != user_id:
            raise http_forbidden_error
        user = await UserService.update_user(user_id=user_id, data=body)
        return user
    except HTTPException as e:
        raise e
    except Exception:
        raise InternalServerError


@router.delete("/{user_id}/", response_model=SUser)
async def delete_user(
    user_id: uuid.UUID,
    current_user: SUser = Depends(UserService.get_current_user),
) -> SUser:
    try:
        if current_user.role != Role.ADMIN and current_user.user_id != user_id:
            raise http_forbidden_error
        user = await UserService.delete_user_by_id(user_id=user_id)
        return user
    except HTTPException as e:
        raise e
    except Exception:
        raise InternalServerError
