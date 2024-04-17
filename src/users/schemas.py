"""This module contains the schemas used to serialize and deserialize data for the users API.

Classes:
    SUser: Pydantic schema representing a user.

Attributes:
    None

"""

import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, constr

from src.users.models import Role

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class BaseModelConfig(BaseModel):
    """BaseModelConfig.

    Base configuration for BaseModel.
    It defines a `model_config` attribute, which is a ConfigDict
    containing the attributes of the model.

    Attributes:
        model_config (ConfigDict): A ConfigDict containing the attributes of the model.
    """

    model_config = ConfigDict(from_attributes=True)


class SCreateUser(BaseModelConfig):
    """CreateUser schema.

    This schema is used to serialize and deserialize the data
    for creating a new user.

    Attributes:
        name (str): The user's name.
        email (EmailStr): The user's email.
        username (str): The user's username.
        hashed_password (str): The user's hashed password.

    """

    name: str
    email: EmailStr
    username: str
    hashed_password: str


class SUser(BaseModelConfig):
    """
    The User schema.

    This schema is used to serialize and deserialize the data
    for a user.

    Attributes:
        user_id (UUID): The unique identifier of the user.
        name (str): The name of the user.
        email (EmailStr): The email address of the user.
        username (str): The username of the user.
        role (Role): The role of the user.
    """

    user_id: UUID
    name: str
    email: EmailStr
    username: str
    role: Role


class SUpdateUser(BaseModelConfig):
    """
    UpdateUser schema.

    This schema is used to serialize and deserialize the data
    for updating a user.

    Attributes:
        name (Optional[str]): The user's name. If not provided, default to None.
        email (Optional[EmailStr]): The user's email. If not provided, default to None.
        hashed_password (Optional[str]): The user's hashed password. If not provided, default to None.

    """

    name: constr(strip_whitespace=True, min_length=1) | None = None
    email: EmailStr | None = None
    hashed_password: constr(min_length=5) | None = None
