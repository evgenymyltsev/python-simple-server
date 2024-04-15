from unittest.mock import AsyncMock

import pytest

from src.database import get_session
from src.main import app

mock_session = AsyncMock()


def override_get_db():
    try:
        yield mock_session
    finally:
        pass


app.dependency_overrides[get_session] = override_get_db


@pytest.fixture
def mock_db_session():
    return mock_session
