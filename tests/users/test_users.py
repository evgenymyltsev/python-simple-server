from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


# Не работает. Не подставляется дефолтное значение
# user_id и role при создании пользователя
def _test_create_product(mock_db_session):

    response = client.post(
        "/users/create",
        json={
            "name": "Misha",
            "email": "misha@test.com",
            "username": "mishatest",
            "hashed_password": "password",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["description"] == "Test Description"

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()
