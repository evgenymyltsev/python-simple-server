from httpx import AsyncClient


async def test_add_user(ac: AsyncClient):
    response = await ac.post(
        "/users",
        json={
            "name": "Misha",
            "email": "misha@test.com",
            "username": "mishatest",
            "hashed_password": "password",
        },
    )
    assert response.status_code == 200


async def test_get_users_unauthorized(ac: AsyncClient):
    response = await ac.get(
        "/users",
    )
    print(response)
    assert response.status_code == 401
