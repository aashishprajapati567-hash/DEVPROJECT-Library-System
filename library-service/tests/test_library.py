from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_token():
    response = client.post(
        "/auth/login",
        data={
            "username": "librarian",
            "password": "library123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Library Microservice is running"


def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "librarian",
            "password": "library123"
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


def test_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200


def test_get_books():
    token = get_token()

    response = client.get(
        "/books/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)