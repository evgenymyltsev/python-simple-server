import uuid
from typing import Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings
from src.auth.schemas import Token, TokenData
from src.database import get_session
from src.users.models import UserOrm
from src.users.schemas import SCreateUser, SUpdateUser, SUser
from src.users.utils import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserService:
    @classmethod
    async def get_current_user(
        cls,
        token: Token = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session),
    ) -> Union[SUser, None]:
        payload = jwt.decode(
            token, settings.auth.secret_key, algorithms=[settings.auth.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        user_model = await cls.get_user_by_field(
            field="username", value=token_data.username, session=session
        )
        if user_model is None:
            return None
        user = SUser.model_validate(user_model)
        return user

    @classmethod
    async def add_user(cls, data: SCreateUser, session: AsyncSession) -> uuid.UUID:
        user_dict = data.model_dump()
        new_user = UserOrm(
            name=user_dict["name"],
            email=user_dict["email"],
            username=user_dict["username"].lower(),
            hashed_password=Hasher.get_password_hash(user_dict["hashed_password"]),
        )

        async with session.begin():
            session.add(new_user)
            await session.flush()
            await session.commit()
            return new_user.user_id

    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> list[SUser]:
        async with session.begin():
            query = select(UserOrm)
            result = await session.execute(query)
            users_model = result.scalars().all()
            users = [SUser.model_validate(user) for user in users_model]
            return users

    @classmethod
    async def update_user(
        cls, user_id: uuid.UUID, data: SUpdateUser, session: AsyncSession
    ) -> Union[SUser, None]:
        async with session.begin():
            user_dict = data.model_dump(exclude_none=True)
            stmt = (
                update(UserOrm)
                .where(UserOrm.user_id == user_id)
                .values(**user_dict)
                .returning(UserOrm)
            )
            result = await session.execute(stmt)
            user_model = result.scalars().first()
            user = SUser.model_validate(user_model)
            return user

    @classmethod
    async def delete_user(cls, user_id: uuid.UUID, session: AsyncSession):
        async with session.begin():
            query = select(UserOrm).where(UserOrm.user_id == user_id)
            result = await session.execute(query)
            user = result.scalar()
            await session.delete(user)
            await session.commit()
            return user.user_id

    @classmethod
    async def delete_user_by_id(cls, user_id: uuid.UUID, session: AsyncSession):
        async with session.begin():
            query = select(UserOrm).where(UserOrm.user_id == user_id)
            result = await session.execute(query)
            user = result.scalar()
            await session.delete(user)
            await session.commit()
            return user.user_id

    @classmethod
    async def get_user_by_field(
        cls, field: str, value: Union[str, uuid.UUID], session: AsyncSession
    ):
        async with session.begin():
            query = select(UserOrm).where(getattr(UserOrm, field) == value)
            result = await session.execute(query)
            user = result.scalar()
            return user
