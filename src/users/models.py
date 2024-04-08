import enum
from uuid import uuid4

from sqlalchemy import TIMESTAMP, Boolean, Enum, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from src.database import Base


class Role(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserOrm(Base):
    __tablename__ = "user"

    user_id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    username = mapped_column(String, nullable=False, unique=True)
    disabled = mapped_column(Boolean, default=False)
    hashed_password = mapped_column(String, nullable=False)
    register_at = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("TIMEZONE('utc', now())"),
    )
    role = mapped_column(Enum(Role), default=Role.USER, nullable=False)
