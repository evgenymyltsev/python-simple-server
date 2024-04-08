from typing import Annotated, Generator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import DB_URL

metadata = MetaData()

# str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    metadata = metadata
    # type_annotation_map = {str_256: String(256)}


engine = create_async_engine(DB_URL, future=True, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
