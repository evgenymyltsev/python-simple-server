from datetime import timedelta

import pytest

from src.utils.jwt import create_access_token, get_tokens


@pytest.fixture
def sample_data():
    return {
        "username": "test_user",
    }


def test_create_access_token():
    data = {"sub": "test_user"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta)
    assert isinstance(token, str)


def test_get_tokens(sample_data):
    username = sample_data["username"]
    tokens = get_tokens(username)
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"
