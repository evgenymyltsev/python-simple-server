import re
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, constr, field_validator

from src.users.models import Role

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class BaseModelConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SCreateUser(BaseModelConfig):
    name: str
    email: EmailStr
    username: str
    hashed_password: str

    @field_validator("name", "username")
    def validate_letters(self, value: str) -> str:
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail=" must contain only letters",
            )
        return value

    @field_validator("hashed_password")
    def validate_hashed_password(self, value: str) -> str:
        if len(value) < 5:
            raise HTTPException(
                status_code=422,
                detail="Hashed password must be at least 5 characters long",
            )
        return value


class SUser(BaseModelConfig):
    user_id: UUID
    name: str
    email: EmailStr
    username: str
    role: Role


class SUpdateUser(BaseModelConfig):
    name: constr(strip_whitespace=True, min_length=1) | None = None
    email: EmailStr | None = None
    hashed_password: constr(min_length=5) | None = None
