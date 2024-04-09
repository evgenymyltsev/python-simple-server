import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.error import InternalServerError
from src.logger import logger
from src.users.models import Role
from src.users.schemas import SCreateUser, SUpdateUser, SUser
from src.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("", response_model=uuid.UUID)
async def create_user(
    body: SCreateUser,
    session: AsyncSession = Depends(get_session),
) -> uuid.UUID:
    try:
        existing_user = await UserService.get_user_by_field(
            field="email", value=body.email, session=session
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "detail": "User with this email already exists",
                    "data": None,
                },
            )
        user_id = await UserService.add_user(data=body, session=session)
        return user_id
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError


@router.get("/{user_id}/", response_model=SUser)
async def get_user_by_id(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    try:
        user = await UserService.get_user_by_field(
            field="user_id", value=user_id, session=session
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "detail": "User not found",
                },
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise InternalServerError(e)


@router.get("", response_model=list[SUser])
async def get_all_users(
    session: AsyncSession = Depends(get_session),
    current_user: SUser = Depends(UserService.get_current_user),
) -> list[SUser]:
    try:
        if current_user.role != Role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": status.HTTP_403_FORBIDDEN,
                    "data": None,
                    "detail": "Only admin can get all users",
                },
            )
        users = await UserService.get_all_users(session=session)
        return users
    except HTTPException as e:
        raise e
    except Exception as e:
        raise InternalServerError(e)


@router.patch("/{user_id}/")
async def update_user(
    user_id: uuid.UUID,
    body: SUpdateUser,
    session: AsyncSession = Depends(get_session),
    current_user: SUser = Depends(UserService.get_current_user),
) -> SUser:
    try:
        if current_user.role != Role.ADMIN and current_user.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only current user or admin can update",
            )
        user = await UserService.update_user(
            user_id=user_id, data=body, session=session
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise InternalServerError(e)


@router.delete("/{user_id}/")
async def delete_user(
    user_id: uuid.UUID,
    current_user: SUser = Depends(UserService.get_current_user),
    session: AsyncSession = Depends(get_session),
) -> uuid.UUID:
    try:
        if current_user.role != Role.ADMIN and current_user.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only current user or admin can delete",
            )
        user_id = await UserService.delete_user(user_id=user_id, session=session)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user_id
    except HTTPException as e:
        raise e
    except Exception as e:
        raise InternalServerError(e)
