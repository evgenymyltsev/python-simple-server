"""The `UsersService` class provides a service layer for handling user related operations."""

import uuid

from src.models.users import UserOrm
from src.repositories.users import UsersRepository
from src.schemas.users import SCreateUser, SUpdateUser
from src.utils.hasher import Hasher


class UsersService:
    """
    The `UsersService` class provides a service layer for handling user related operations.

    Attributes:
        users_repo (UsersRepository): An instance of `UsersRepository` for users.

    Methods:
        add_user(user: SCreateUser) -> UserOrm:
            Adds a new user.

        get_user(filter_by: dict) -> UserOrm:
            Retrieves a user based on the filter parameters.

        get_auth_user(username: str, password: str) -> UserOrm:
            Retrieves a user based on the provided credentials for authentication.

        get_all_users() -> list[UserOrm]:
            Retrieves all users.

        delete_user(user_id: uuid.UUID) -> UserOrm:
            Deletes a user specified by the `user_id` parameter.

        update_user(filter_by: dict, data: SUpdateUser) -> UserOrm:
            Updates a user based on the provided filter and data.
    """

    def __init__(self: "UsersService", users_repo: UsersRepository) -> None:
        """Initialize a new instance of the `UsersService` class.

        Args:
            users_repo (UsersRepository): The repository to use for
                interacting with the users.
        """
        self.users_repo: UsersRepository = users_repo()

    async def add_user(self: "UsersService", user: SCreateUser) -> UserOrm:
        """Add a new user.

        Args:
            user (SCreateUser): The user to be added.

        Returns:
            UserOrm: The created user.
        """
        user_dict = user.model_dump()
        user = await self.users_repo.add_one(user_dict)
        return user

    async def get_user(self: "UsersService", filter_by: dict) -> UserOrm:
        """Retrieve a user based on the filter parameters.

        Args:
            filter_by (dict): The filter parameters.

        Returns:
            UserOrm: The user object matching the filter, or None if not found.
        """
        user = await self.users_repo.find_one(filter_by)
        return user

    async def get_auth_user(self: "UsersService", username: str, password: str) -> UserOrm:
        """Retrieve a user based on the provided credentials for authentication.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            UserOrm: The user object if the credentials are valid, else None.
        """
        user = await self.users_repo.find_one({"username": username})
        if user is None or not Hasher.verify_password(password, user.hashed_password):
            return None
        return user

    async def get_all_users(self: "UsersService") -> UserOrm:
        """Retrieve all users.

        Returns:
            list[UserOrm]: A list of all users. If no users are found, an empty list is returned.
        """
        users = await self.users_repo.find_all()
        return users

    async def delete_user(self: "UsersService", user_id: uuid.UUID) -> UserOrm:
        """Delete a user specified by the `user_id` parameter.

        Args:
            user_id (uuid.UUID): The UUID of the user to delete.

        Returns:
            UserOrm: The deleted user object.
        """
        user = await self.users_repo.delete_one({"user_id": user_id})
        return user

    async def update_user(self: "UsersService", filter_by: dict, data: SUpdateUser) -> UserOrm:
        """Update a user based on the provided filter and data.

        Args:
            filter_by (dict): A dictionary specifying the fields to search by.
            data (SUpdateUser): An object containing the data to update the user with.

        Returns:
            UserOrm: The updated user object.
        """
        values = None
        if type(data) is not dict:
            values = data.model_dump(exclude_none=True)
        values = data
        user = await self.users_repo.update_one(filter_by, values)
        return user
