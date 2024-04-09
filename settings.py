from envparse import Env
from pydantic_settings import BaseSettings

env = Env()
env.read_envfile()


class AuthSettings(BaseSettings):
    secret_key: str = env.str("SECRET_KEY")
    algorithm: str = env.str("ALGORITHM")
    access_token_expires_minutes: int = env.int("ACCESS_TOKEN_EXPIRES_MINUTES")
    refresh_token_expires_minutes: int = env.int("REFRESH_TOKEN_EXPIRES_MINUTES")


class DBSettings(BaseSettings):
    url: str = env.str("DB_URL")
    pg_dsn: str = env.str("PG_DSN")


class RedisSettings(BaseSettings):
    redis_dsn: str = env.str("REDIS_DSN")


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()
