import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Create a separate in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(autouse=True)
def setup_test_database():
    # Create fresh tables before every test
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield

    # Clean everything after every test
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


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