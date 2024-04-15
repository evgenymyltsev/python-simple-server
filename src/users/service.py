import uuid

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import select, update

from settings import settings
from src.auth.schemas import SToken, STokenData
from src.database import async_session
from src.users.models import UserOrm
from src.users.schemas import SCreateUser, SUpdateUser, SUser
from src.users.utils import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserService:
    @classmethod
    async def get_current_user(
        cls,
        token: SToken = Depends(oauth2_scheme),
    ) -> SUser | None:
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        username: str = payload.get("sub")
        token_data = STokenData(username=username)
        user_model = await cls.get_user_by_field(field="username", value=token_data.username)
        user = SUser.model_validate(user_model)
        return user

    @classmethod
    async def add_user(
        cls,
        data: SCreateUser,
    ) -> SUser | None:
        user_dict = data.model_dump()
        new_user_model = UserOrm(
            name=user_dict["name"],
            email=user_dict["email"],
            username=user_dict["username"].lower(),
            hashed_password=Hasher.get_password_hash(user_dict["hashed_password"]),
        )
        async with async_session() as session:
            async with session.begin():
                session.add(new_user_model)
                await session.flush()
                await session.commit()
                user = SUser.model_validate(new_user_model)
            return user

    @classmethod
    async def get_all_users(
        cls,
    ) -> SUser | None:
        async with async_session() as session:
            async with session.begin():
                query = select(UserOrm)
                result = await session.execute(query)
                users_model = result.scalars()
                users = [SUser.model_validate(user) for user in users_model]
                return users

    @classmethod
    async def update_user(
        cls,
        user_id: uuid.UUID,
        data: SUpdateUser,
    ) -> SUser | None:
        async with async_session() as session:
            async with session.begin():
                user_dict = data.model_dump(exclude_none=True)
                stmt = update(UserOrm).where(UserOrm.user_id == user_id).values(**user_dict).returning(UserOrm)
                result = await session.execute(stmt)
                user_model = result.scalar()
                user = SUser.model_validate(user_model)
                return user

    @classmethod
    async def delete_user_by_id(
        cls,
        user_id: uuid.UUID,
    ) -> SUser | None:
        async with async_session() as session:
            async with session.begin():
                query = select(UserOrm).where(UserOrm.user_id == user_id)
                result = await session.execute(query)
                user_model = result.scalar_one()
                await session.delete(user_model)
                await session.commit()
                user = SUser.model_validate(user_model)
                return user

    @classmethod
    async def get_user_by_field(
        cls,
        field: str,
        value: str | uuid.UUID,
    ) -> SUser | None:
        async with async_session() as session:
            async with session.begin():
                query = select(UserOrm).where(getattr(UserOrm, field) == value)
                result = await session.execute(query)
                user_model = result.scalar_one()
                user = SUser.model_validate(user_model)
                return user
