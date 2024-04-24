"""
Module contains Pydantic models used to define the authentication API's request and response payloads.

The models defined in this package are:

- `SToken`: Pydantic model representing a JSON Web Token.
- `SRefreshToken`: Pydantic model representing a refresh token.

"""

from pydantic import BaseModel


class SToken(BaseModel):
    """
    SToken is a Pydantic model representing a JSON Web Token.

    Attributes:
        access_token (str): The access token string.
        refresh_token (str): The refresh token string.
        token_type (str): The type of the token.
    """

    access_token: str
    refresh_token: str
    token_type: str


class SRefreshToken(BaseModel):
    """
    SRefreshToken is a Pydantic model representing a refresh token.

    Attributes:
        refresh_token (str): The refresh token string.
    """

    refresh_token: str


class STokenData(BaseModel):
    """
    STokenData is a Pydantic model representing data used to create a token.

    Attributes:
        username (str | None): The username for the token. Defaults to None.

    """

    username: str | None = None
