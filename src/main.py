from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.router import router as auth_router
from src.cache import Cache
from src.users.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Cache.get_redis_client()
    print("redis has connected")
    yield
    Cache.close_redis_client()
    print("redis has stopped")


app = FastAPI(title="Auth Simple Server", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    # dev only
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

app.include_router(user_router)
app.include_router(auth_router)