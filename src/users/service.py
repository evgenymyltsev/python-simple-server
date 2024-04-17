"""
User Service Module.

This module contains the User Service class which provides methods for interacting with the User database.

This module contains the following classes:

- `UserService`: A class that provides methods for interacting with the User database.

This module contains the following exceptions:

- `None`: This exception is raised when a method is called with invalid arguments.

"""

import uuid
from typing import Type

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, update

from src.auth.schemas import SToken, STokenData
from src.auth.utils import jwt_decode
from src.database import async_session
from src.users.models import UserOrm
from src.users.schemas import SCreateUser, SUpdateUser, SUser
from src.users.utils import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserService:
    """The UserService class provides methods for interacting with the User database.

    It contains the following public methods:

    - `add_user`: Adds a new user to the database.
    - `get_all_users`: Retrieves all users from the database.
    - `get_user_by_field`: Retrieves a user from the database by a specified field.
    - `get_current_user`: Retrieves the current user from the database using an access token.
    - `update_user`: Updates a user in the database.
    - `update_email_verified`: Updates the email_verified field of a user in the database.
    - `delete_user_by_id`: Deletes a user from the database by their ID.


    Note:
        This class is not meant to be instantiated.

    """

    @classmethod
    async def get_current_user(
        cls: Type["UserService"],
        token: SToken = Depends(oauth2_scheme),
    ) -> SUser | None:
        """Retrieve the current user from the database using an access token.

        Args:
            token (SToken, optional): The access token used to authenticate the request.
                Defaults to Depends(oauth2_scheme).

        Returns:
            SUser | None: The current user, or None if the access token is invalid.
        """
        payload = jwt_decode(token)
        username: str = payload.get("sub")
        token_data = STokenData(username=username)
        user_model = await cls.get_user_by_field(field="username", value=token_data.username)
        user = SUser.model_validate(user_model)
        return user

    @classmethod
    async def add_user(
        cls: Type["UserService"],
        data: SCreateUser,
    ) -> SUser | None:
        """Add a new user to the database.

        Args:
            data (SCreateUser): The user data to be added.

        Returns:
            SUser or None: The newly created user, or None if the operation fails.
        """
        user_dict = data.model_dump()
        new_user_model = UserOrm(
            name=user_dict["name"],
            email=user_dict["email"],
            username=user_dict["username"].lower(),
            hashed_password=Hasher.get_password_hash(user_dict["hashed_password"]),
        )
        async with async_session() as session:
            async with session.begin():
                session.add(new_user_model)
                await session.flush()
                await session.commit()
                user = SUser.model_validate(new_user_model)
            return user

    @classmethod
    async def get_all_users(
        cls: Type["UserService"],
    ) -> SUser | None:
        """Retrieve all users from the database.

        This function uses an asynchronous session to execute a SELECT query
        against the UserOrm model. It retrieves all UserOrm instances from
        the database and converts them to SUser instances using the
        SUser.model_validate() method.

        Returns:
            List[SUser] | None: A list of all users in the database, or None
            if the operation fails.
        """
        async with async_session() as session:
            async with session.begin():
                query = select(UserOrm)
                result = await session.execute(query)
                users_model = result.scalars()
                users = [SUser.model_validate(user) for user in users_model]
                return users

    @classmethod
    async def update_user(
        cls: Type["UserService"],
        user_id: uuid.UUID,
        data: SUpdateUser,
    ) -> SUser | None:
        """Update a user in the database.

        Args:
            user_id (uuid.UUID): The ID of the user to update.
            data (SUpdateUser): The data to update the user with.

        Returns:
            SUser or None: The updated user, or None if the operation fails.
        """
        async with async_session() as session:
            async with session.begin():
                user_dict = data.model_dump(exclude_none=True)
                stmt = update(UserOrm).where(UserOrm.user_id == user_id).values(**user_dict).returning(UserOrm)
                result = await session.execute(stmt)
                user_model = result.scalar()
                user = SUser.model_validate(user_model)
                return user

    @classmethod
    async def update_email_verified(
        cls: Type["UserService"],
        email: str,
        is_verified: bool,
    ) -> SUser | None:
        """Update the 'email_verified' field of a user with the given email.

        Args:
            email (str): The email of the user to update.
            is_verified (bool): The new value for the 'email_verified' field.

        Returns:
            SUser or None: The updated user, or None if the operation fails.

        """
        async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(UserOrm).where(UserOrm.email == email).values(email_verified=is_verified).returning(UserOrm)
                )
                result = await session.execute(stmt)
                user_model = result.scalar()
                user = SUser.model_validate(user_model)
                return user

    @classmethod
    async def delete_user_by_id(
        cls: Type["UserService"],
        user_id: uuid.UUID,
    ) -> SUser | None:
        """Delete a user from the database by ID.

        Args:
            user_id (uuid.UUID): The ID of the user to be deleted.

        Returns:
            SUser or None: The deleted user, or None if the operation fails.
        """
        async with async_session() as session:
            async with session.begin():
                query = select(UserOrm).where(UserOrm.user_id == user_id)
                result = await session.execute(query)
                user_model = result.scalar_one()
                await session.delete(user_model)
                await session.commit()
                user = SUser.model_validate(user_model)
                return user

    @classmethod
    async def get_user_by_field(
        cls: Type["UserService"],
        field: str,
        value: str | uuid.UUID,
    ) -> SUser | None:
        """Retrieve a user from the database by a specific field and its value.

        Args:
            field (str): The name of the field to query against.
            value (str or uuid.UUID): The value to match against the specified field.

        Returns:
            SUser or None: The user matching the specified field and value, or None if no user is found.

        Raises:
            NoResultFound: If no user is found with the given field and value.

        """
        async with async_session() as session:
            async with session.begin():
                query = select(UserOrm).where(getattr(UserOrm, field) == value)
                result = await session.execute(query)
                user_model = result.scalar_one()
                user = SUser.model_validate(user_model)
                return user
