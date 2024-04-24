"""This module contains the entry point of the application.

It sets up the FastAPI application and defines the routes for authentication and user management.

Attributes:
    app (FastAPI): The FastAPI application instance.

"""

from typing import Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from logger import get_logger
from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.cache import Cache

logger = get_logger(__name__)


async def lifespan(app: FastAPI) -> Generator:
    """Provide lifespan functionality.

    This function is called when the app is started and when it is shut down.
    It yields control and performs the necessary setup and teardown operations.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None

    Returns:
        Generator: A generator object that yields control.

    """
    Cache.get_redis_client()
    logger.critical("redis has connected")
    yield
    Cache.close_redis_client()
    logger.critical("redis has stopped")


app = FastAPI(title="Auth Simple Server", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app.include_router(auth_router)
app.include_router(users_router)
