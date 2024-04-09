from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.database import Base, get_session
from src.main import app
from tests.settings import settings


engine_test = create_async_engine(
    settings.db.pg_dsn_test, poolclass=NullPool, echo=True
)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True, scope="session")
async def init_db() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        # При запуске тестов warning, что устаревший подход
        # async with AsyncClient(app=app, base_url="http://test") as ac:
        # поменял на такой, но ничего не поменялось
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


def run():
    pytest.main(["-v"])
