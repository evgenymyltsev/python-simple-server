from envparse import Env
from pydantic_settings import BaseSettings

env = Env()
env.read_envfile()


class DBSettings(BaseSettings):
    url_test: str = env.str("DB_URL_TEST")
    pg_dsn_test: str = env.str("PG_DSN_TEST")


class Settings(BaseSettings):
    db: DBSettings = DBSettings()


settings = Settings()
