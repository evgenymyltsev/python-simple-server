import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from logger import get_logger
from src.database import get_session
from src.error import InternalServerError
from src.users.models import Role, UserOrm
from src.users.schemas import SCreateUser, SUpdateUser, SUser
from src.users.service import UserService
from src.users.utils import Hasher

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

http_forbidden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Only admin or current user can perform this action",
)

logger = get_logger(__name__)


@router.post("", response_model=SUser)
async def create_user(
    body: SCreateUser,
) -> SUser:
    try:
        user = await UserService.add_user(data=body)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError


# for testing Depends(get_session) start
# for testing Depends(get_session) start
@router.post("/create", response_model=SUser)
async def create_user_test(body: SCreateUser, session: AsyncSession = Depends(get_session)) -> SUser:
    try:
        user_dict = body.model_dump()
        new_user_model = UserOrm(
            name=user_dict["name"],
            email=user_dict["email"],
            username=user_dict["username"].lower(),
            hashed_password=Hasher.get_password_hash(user_dict["hashed_password"]),
        )
        session.add(new_user_model)
        await session.flush()
        await session.commit()
        user = SUser.model_validate(new_user_model)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError


# for testing Depends(get_session) end


@router.get("/{user_id}/", response_model=SUser)
async def get_user_by_id(
    user_id: uuid.UUID,
) -> SUser:
    try:
        user = await UserService.get_user_by_field(field="user_id", value=user_id)
        return user
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
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
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
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
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
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
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError
