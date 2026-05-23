import pytest


@pytest.mark.anyio
async def test_create_user(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "user",
        "active": True,
    }

    res = await client.post("/api/v1/users/", json=payload)

    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.anyio
async def test_list_users(client):
    res = await client.get("/api/v1/users/")

    assert res.status_code == 200
    data = res.json()

    assert "items" in data
    assert "total" in data


@pytest.mark.anyio
async def test_health(client):
    res = await client.get("/health")
    assert res.status_code == 200