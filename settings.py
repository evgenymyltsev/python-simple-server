from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AuthSettings(SettingsConfig):
    secret_key: str = Field("", env="SECRET_KEY")
    algorithm: str = Field("", env="ALGORITHM")
    access_token_expires_minutes: int = Field(2, env="ACCESS_TOKEN_EXPIRES_MINUTES")
    refresh_token_expires_minutes: int = Field(8, env="REFRESH_TOKEN_EXPIRES_MINUTES")


class DBSettings(SettingsConfig):
    db_url: str = Field("", env="DB_URL")
    pg_dsn: str = Field("", env="PG_DSN")


class RedisSettings(SettingsConfig):
    redis_dsn: str = Field("", env="REDIS_DSN")


class Settings(SettingsConfig):
    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()
