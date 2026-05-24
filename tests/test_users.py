import pytest


def test_create_user(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "user",
        "active": True,
    }

    res = client.post("/api/v1/users/", json=payload)

    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
    assert "id" in data


def test_create_user_duplicate_username(client):
    payload = {
        "username": "duplicate",
        "email": "one@example.com",
        "first_name": "First",
        "last_name": "One",
        "role": "user",
        "active": True,
    }

    client.post("/api/v1/users/", json=payload)
    res = client.post(
        "/api/v1/users/",
        json={**payload, "email": "two@example.com"},
    )

    assert res.status_code == 409
    assert res.json()["detail"] == "User with this username already exists"


def test_create_user_duplicate_email(client):
    payload = {
        "username": "firstuser",
        "email": "duplicate@example.com",
        "first_name": "First",
        "last_name": "User",
        "role": "user",
        "active": True,
    }

    client.post("/api/v1/users/", json=payload)
    res = client.post(
        "/api/v1/users/",
        json={**payload, "username": "seconduser"},
    )

    assert res.status_code == 409
    assert res.json()["detail"] == "User with this email already exists"


def test_get_user_by_id(client):
    payload = {
        "username": "getuser",
        "email": "getuser@example.com",
        "first_name": "Get",
        "last_name": "User",
        "role": "user",
        "active": True,
    }

    create_res = client.post("/api/v1/users/", json=payload)
    user_id = create_res.json()["id"]

    res = client.get(f"/api/v1/users/{user_id}")

    assert res.status_code == 200
    data = res.json()
    assert data["id"] == user_id
    assert data["username"] == "getuser"


def test_get_user_not_found(client):
    res = client.get("/api/v1/users/000000000000000000000000")

    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"


def test_invalid_user_id_returns_404(client):
    res = client.get("/api/v1/users/invalid-id")

    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"


def test_update_user(client):
    payload = {
        "username": "updateuser",
        "email": "updateuser@example.com",
        "first_name": "Update",
        "last_name": "User",
        "role": "user",
        "active": True,
    }

    create_res = client.post("/api/v1/users/", json=payload)
    user_id = create_res.json()["id"]

    update_res = client.put(
        f"/api/v1/users/{user_id}",
        json={"first_name": "Updated", "active": False},
    )

    assert update_res.status_code == 200
    data = update_res.json()
    assert data["first_name"] == "Updated"
    assert data["active"] is False


def test_delete_user(client):
    payload = {
        "username": "deleteuser",
        "email": "deleteuser@example.com",
        "first_name": "Delete",
        "last_name": "User",
        "role": "user",
        "active": True,
    }

    create_res = client.post("/api/v1/users/", json=payload)
    user_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/v1/users/{user_id}")

    assert delete_res.status_code == 204

    get_res = client.get(f"/api/v1/users/{user_id}")
    assert get_res.status_code == 404


def test_get_users_filters(client):
    users = [
        {
            "username": "adminuser",
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "role": "admin",
            "active": True,
        },
        {
            "username": "guestuser",
            "email": "guest@example.com",
            "first_name": "Guest",
            "last_name": "User",
            "role": "guest",
            "active": False,
        },
    ]

    for user in users:
        client.post("/api/v1/users/", json=user)

    res = client.get("/api/v1/users/?role=admin&active=true")

    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["role"] == "admin"
    assert data["items"][0]["active"] is True


def test_list_users_pagination(client):
    for index in range(5):
        client.post(
            "/api/v1/users/",
            json={
                "username": f"user{index}",
                "email": f"user{index}@example.com",
                "first_name": "User",
                "last_name": str(index),
                "role": "user",
                "active": True,
            },
        )

    res = client.get("/api/v1/users/?limit=2&skip=2")

    assert res.status_code == 200
    data = res.json()
    assert data["limit"] == 2
    assert data["skip"] == 2
    assert len(data["items"]) == 2


def test_create_user_extra_fields_rejected(client):
    payload = {
        "username": "extrauser",
        "email": "extra@example.com",
        "first_name": "Extra",
        "last_name": "Field",
        "role": "user",
        "active": True,
        "unexpected": "value",
    }

    res = client.post("/api/v1/users/", json=payload)

    assert res.status_code == 422
    assert "detail" in res.json()


def test_update_user_invalid_payload(client):
    payload = {
        "username": "updatetest",
        "email": "updatetest@example.com",
        "first_name": "Update",
        "last_name": "Test",
        "role": "user",
        "active": True,
    }

    create_res = client.post("/api/v1/users/", json=payload)
    user_id = create_res.json()["id"]

    res = client.put(
        f"/api/v1/users/{user_id}",
        json={"active": "not-a-boolean"},
    )

    assert res.status_code == 422
    assert "detail" in res.json()


def test_delete_user_not_found(client):
    res = client.delete("/api/v1/users/000000000000000000000000")

    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"


def test_list_users_invalid_query_params(client):
    res = client.get("/api/v1/users/?limit=-1&active=notabool")

    assert res.status_code == 422
    assert "detail" in res.json()


def test_create_user_invalid_payload(client):
    payload = {
        "username": "baduser",
        "email": "not-an-email",
        "first_name": "Bad",
        "last_name": "User",
        "role": "user",
        "active": True,
    }

    res = client.post("/api/v1/users/", json=payload)

    assert res.status_code == 422
    assert "detail" in res.json()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
