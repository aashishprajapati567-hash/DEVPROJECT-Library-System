from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_token():
    response = client.post(
        "/auth/login",
        data={
            "username": "inventoryadmin",
            "password": "inventory123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Inventory Microservice is running"


def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "inventoryadmin",
            "password": "inventory123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "wrong",
            "password": "wrong"
        }
    )

    assert response.status_code == 401


def test_get_inventory():
    token = get_token()

    response = client.get(
        "/inventory/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_inventory():
    token = get_token()

    response = client.post(
        "/inventory/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "book_id": 999999,
            "total_copies": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["book_id"] == 999999
    assert data["total_copies"] == 5
    assert data["available_copies"] == 5