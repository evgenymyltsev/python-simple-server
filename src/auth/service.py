from typing import Union

from sqlalchemy import select

from src.database import async_session
from src.users.models import UserOrm
from src.users.schemas import SUser
from src.users.utils import Hasher


class AuthService:
    @classmethod
    async def get_user(cls, username: str, password: str) -> Union[SUser, None]:
        async with async_session() as session:
            async with session.begin():
                query = select(UserOrm).where(UserOrm.username == username)
                result = await session.execute(query)
                user_model = result.scalar()
                if user_model is None or not Hasher.verify_password(
                    password, user_model.hashed_password
                ):
                    return None
                user = SUser.model_validate(user_model)
                return user
