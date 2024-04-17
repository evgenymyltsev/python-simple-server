"""User API router.

This module contains the API routes related to user management.

"""

import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from logger import get_logger
from src.email.tasks import send_email
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

logger = get_logger(__name__)


@router.post("", response_model=SUser)
async def create_user(
    background_tasks: BackgroundTasks,
    body: SCreateUser,
) -> SUser:
    """Create a new user.

    Args:
        body (SCreateUser): The user data to be created.

    Returns:
        SUser: The newly created user.

    Raises:
        HTTPException: If there is an error during the user creation.

    """
    try:
        user = await UserService.add_user(data=body)
        user_dict = body.model_dump()
        background_tasks.add_task(send_email, user_dict["username"], user_dict["email"])
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError


@router.get("/{user_id}/", response_model=SUser)
async def get_user_by_id(
    user_id: uuid.UUID,
) -> SUser:
    """Get user by ID.

    This function retrieves a user by their unique ID.

    Args:
        user_id (uuid.UUID): The UUID of the user.

    Returns:
        SUser: The user object.

    Raises:
        HTTPException: If there is an error during the user retrieval.

    """
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
    """Get all users.

    This function retrieves all users. This endpoint is only accessible to users with the role ADMIN.

    Args:
        current_user (SUser): The currently authenticated user.

    Returns:
        list[SUser]: A list of user objects.

    Raises:
        HTTPException: If the user does not have the role ADMIN or if there is an error during the user retrieval.

    """
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
    """Update a user.

    This function updates a user's information. This endpoint is only accessible to users with the role ADMIN.

    Args:
        user_id (uuid.UUID): The UUID of the user to update.
        body (SUpdateUser): The updated user information.
        current_user (SUser): The currently authenticated user.

    Returns:
        SUser: The updated user object.

    Raises:
        HTTPException: If the user does not have the role ADMIN or if there is an error during the user update.

    """
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
    """Delete a user.

    Deletes a user specified by the `user_id` parameter.

    Args:
        user_id (uuid.UUID): The UUID of the user to delete.
        current_user (SUser): The currently authenticated user.

    Returns:
        SUser: The deleted user object.

    Raises:
        HTTPException: If the user does not have the role ADMIN or if there is an error during the user deletion.

    """
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
