"""Module that provides dependencies for the API."""

from src.repositories.users import UsersRepository
from src.services.users import UsersService


def users_service() -> UsersService:
    """
    Create a new `UsersService` instance using the `UsersRepository` and return it.

    Returns:
        `UsersService`: A new instance of the `UsersService` class.

    """
    return UsersService(UsersRepository)
