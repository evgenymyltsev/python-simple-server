"""
Module that contains the `UserOrm` model.

Classes:
    `UserOrm`: The model representing a user in the database.

"""

import enum
from uuid import uuid4

from sqlalchemy import TIMESTAMP, Boolean, Enum, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from src.database import Base


class Role(enum.Enum):
    """An enumeration of the possible roles for a user.

    Attributes:
        USER (str): The role for a regular user.
        ADMIN (str): The role for an admin user.
    """

    USER = "USER"
    ADMIN = "ADMIN"


class UserOrm(Base):
    """
    The UserOrm model represents a user in the database.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        user_id (UUID): The unique identifier of the user.
        name (str): The name of the user.
        email (str): The email address of the user.
        username (str): The username of the user.
        disabled (bool): Indicates if the user is disabled.
        hashed_password (str): The hashed password of the user.
        register_at (datetime): The timestamp when the user registered.
        role (Role): The role of the user.
        email_verified (bool): Indicates if the user's email is verified.
    """

    __tablename__ = "user"

    user_id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = mapped_column(String, nullable=False, info={"validate": {"regex": r"^[а-яА-Яa-zA-Z\-]+$"}})
    email = mapped_column(
        String,
        nullable=False,
        unique=True,
        info={"validate": {"regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"}},
    )
    username = mapped_column(String, nullable=False, unique=True, info={"validate": {"regex": r"^[а-яА-Яa-zA-Z\-]+$"}})
    disabled = mapped_column(Boolean, default=False)
    hashed_password = mapped_column(String, nullable=False)
    register_at = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("TIMEZONE('utc', now())"),
    )
    role = mapped_column(Enum(Role), default=Role.USER, nullable=False)
    email_verified = mapped_column(Boolean, default=False)
