"""User API router.

This module contains the API routes related to user management.

"""

import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from logger import get_logger
from src.api.dependencies import users_service
from src.error import InternalServerError
from src.schemas.users import SCreateUser, SUpdateUser, SUser
from src.services.email import EmailService
from src.services.users import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

logger = get_logger(__name__)


@router.post("", response_model=SUser)
async def create_new_user(
    background_tasks: BackgroundTasks,
    body: SCreateUser,
    users_service: UsersService = Depends(users_service),
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
        user = await users_service.add_user(user=body)
        background_tasks.add_task(EmailService.send_email, body.username, body.email)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError


@router.get("/{user_id}/", response_model=SUser)
async def get_user_by_id(
    user_id: uuid.UUID,
    users_service: UsersService = Depends(users_service),
) -> SUser:
    """Get user by ID.

    This function retrieves a user by their unique ID.

    Args:
        filter_by: user_id (uuid.UUID): The UUID of the user.

    Returns:
        SUser: The user object.

    Raises:
        HTTPException: If there is an error during the user retrieval.

    """
    try:
        user = await users_service.get_user(filter_by={"user_id": user_id})
        return user
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError


@router.get("", response_model=list[SUser])
async def get_all_users(
    users_service: UsersService = Depends(users_service),
) -> list[SUser]:
    """Get all users.

    Retrieves all users from the database and returns them as a list of SUser objects.

    Args:
        users_service (UsersService): An instance of the UsersService class.

    Returns:
        list[SUser]: A list of SUser objects representing all users in the database.

    Raises:
        HTTPException: If there is an error during the user retrieval.
    """
    try:
        users = await users_service.get_all_users()
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
    users_service: UsersService = Depends(users_service),
) -> SUser:
    """Update a user.

    Args:
        user_id (uuid.UUID): The unique id of the user to be updated.
        body (SUpdateUser): The data to update the user with.
        users_service (UsersService): An instance of the UsersService class.

    Returns:
        SUser: The updated user.

    Raises:
        HTTPException: If there is an error during the user update.

    """
    try:
        user = await users_service.update_user({"user_id": user_id}, data=body)
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
    users_service: UsersService = Depends(users_service),
) -> SUser:
    """Delete a user specified by the `user_id` parameter.

    Args:
        user_id (uuid.UUID): The UUID of the user to delete.
        users_service (UsersService): An instance of the UsersService class.

    Returns:
        SUser: The deleted user object.

    Raises:
        HTTPException: If there is an error during the user deletion.

    """
    try:
        user = await users_service.delete_user(user_id=user_id)
        return user
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise InternalServerError
