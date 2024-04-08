import re
from typing import Optional
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
    def validate_letters(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail=f" must contain only letters",
            )
        return value

    @field_validator("hashed_password")
    def validate_hashed_password(cls, value):
        if len(value) < 5:
            raise HTTPException(
                status_code=422,
                detail=f"Hashed password must be at least5 characters long",
            )
        return value


class SUser(BaseModelConfig):
    user_id: UUID
    name: str
    email: EmailStr
    username: str
    role: Role


class SUpdateUser(BaseModelConfig):
    name: Optional[constr(strip_whitespace=True, min_length=1)] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[constr(min_length=5)] = None
