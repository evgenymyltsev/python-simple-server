"""
The `auth` module provides a service for handling authentication-related functionality.

This module contains the following classes:

- `AuthService`: A service class that handles authentication tasks.

The `AuthService` class provides the following methods:

- `get_user`: Retrieve a user from the database by username and password..

"""

from typing import Type

from sqlalchemy import select

from src.database import async_session
from src.users.models import UserOrm
from src.users.schemas import SUser
from src.users.utils import Hasher


class AuthService:
    """The `AuthService` class is a service class that handles authentication tasks.

    This class provides methods for interacting with
    the database to retrieve a user by username and password.
    """

    @classmethod
    async def get_user(
        cls: Type["AuthService"],
        username: str,
        password: str,
    ) -> SUser | None:
        """Retrieve a user from the database by username and password.

        Args:
            username (str): The username of the user to retrieve.
            password (str): The password of the user to retrieve.

        Returns:
            SUser or None: The retrieved user, or None if the user does not exist or the password is incorrect.
        """
        async with async_session() as session:
            async with session.begin():
                query = select(UserOrm).where(UserOrm.username == username)
                result = await session.execute(query)
                user_model = result.scalar()
                if user_model is None or not Hasher.verify_password(password, user_model.hashed_password):
                    return None
                user = SUser.model_validate(user_model)
                return user
