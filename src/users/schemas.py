import re
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, constr

from src.users.models import Role

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class BaseModelConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SCreateUser(BaseModelConfig):
    name: str
    email: EmailStr
    username: str
    hashed_password: str


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
