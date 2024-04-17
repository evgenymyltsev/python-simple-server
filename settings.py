"""
Module containing all application settings.

This module defines various settings used by the application,
such as database connection strings, secret keys, and email
credentials. These settings are used to configure the application
and are typically loaded from environment variables.

Attributes:
    AuthSettings (class): Settings for authentication.
    DBSettings (class): Settings for database connection.
    SmtpSettings (class): Settings for email credentials.

"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsConfig(BaseSettings):
    """Configuration for the application settings.

    Attributes:
        model_config (SettingsConfigDict): The configuration dictionary
            for the settings.

    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AuthSettings(SettingsConfig):
    """Settings for authentication.

    Attributes:
        secret_key (str): The secret key used to sign and verify JWTs.
        algorithm (str): The algorithm used to sign and verify JWTs.
        access_token_expires_minutes (int): The number of minutes an access token is valid.
        refresh_token_expires_minutes (int): The number of minutes a refresh token is valid.

    """

    secret_key: str = Field("", json_schema_extra={"env": "SECRET_KEY"})
    algorithm: str = Field("", json_schema_extra={"env": "ALGORITHM"})
    access_token_expires_minutes: int = Field(2, json_schema_extra={"env": "ACCESS_TOKEN_EXPIRES_MINUTES"})
    refresh_token_expires_minutes: int = Field(8, json_schema_extra={"env": "REFRESH_TOKEN_EXPIRES_MINUTES"})


class DBSettings(SettingsConfig):
    """Settings for database connection.

    Attributes:
        db_url (str): The URL of the database.
        pg_dsn (str): The PostgreSQL dsn (Data Source Name).

    """

    db_url: str = Field("", json_schema_extra={"env": "DB_URL"})
    pg_dsn: str = Field("", json_schema_extra={"env": "PG_DSN"})


class RedisSettings(SettingsConfig):
    """Settings for Redis connection.

    Attributes:
        redis_dsn (str): The Redis dsn (Data Source Name).

    Redis DSN has the following format:
    redis[+transport]://[[user]:[password]@]host[:port][/database][?param1=value1&...].
    """

    redis_dsn: str = Field("", json_schema_extra={"env": "REDIS_DSN"})


class SmtpSettings(SettingsConfig):
    """Settings for email sending.

    Attributes:
        user (str): The email address to send from.
        password (str): The password of the email account.

    Environment Variables:
        email_user (str): The email address to send from.
        email_password (str): The password of the email account.
        email_host (str): The host of the email server.
        email_port (int): The port of the email server.
    """

    email_user: str = Field("", json_schema_extra={"env": "EMAIL_USER"})
    email_password: str = Field("", json_schema_extra={"env": "EMAIL_PASSWORD"})
    email_host: str = Field("", json_schema_extra={"env": "EMAIL_HOST"})
    email_port: int = Field(465, json_schema_extra={"env": "EMAIL_PORT"})


class Settings(SettingsConfig):
    """The global settings object.

    Attributes:
        db (DBSettings): The settings for the database connection.
        redis (RedisSettings): The settings for Redis connection.
        auth (AuthSettings): The settings for authentication.
        email (SmtpSettings): The settings for email sending.
    """

    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()
    smtp: SmtpSettings = SmtpSettings()


settings = Settings()
