"""
Defines a repository for handling operations on user data.

Classes:
    UsersRepository: A subclass of SQLAlchemyRepository that handles operations on UserOrm model instances.

Attributes:
    model (Type[UserOrm]): The model that this repository handles.

"""

from src.models.users import UserOrm
from src.repositories.abstract import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository[UserOrm]):
    """A repository for handling operations on user data.

    Attributes:
        model (Type[UserOrm]): The model that this repository handles.

    This class provides methods for handling common operations on `UserOrm`
    model instances, such as creating, updating, and deleting users.
    """

    model = UserOrm
