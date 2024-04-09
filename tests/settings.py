from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DBSettings(SettingsConfig):
    url_test: str = Field("", env="DB_URL_TEST")
    pg_dsn_test: str = Field("", env="PG_DSN_TEST")


class Settings(BaseSettings):
    db: DBSettings = DBSettings()


settings = Settings()
