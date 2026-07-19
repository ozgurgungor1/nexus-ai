from uuid import uuid4

from fastapi.testclient import TestClient

from backend.main import app


def test_register_and_login() -> None:
    client = TestClient(app)
    email = f"test-{uuid4().hex}@example.com"
    password = "TestPass123!"

    register_response = client.post(
        "/register",
        json={"email": email, "password": password, "full_name": "Test User"},
    )
    assert register_response.status_code == 200
    user_data = register_response.json()
    assert user_data["email"] == email
    assert user_data["role"] == "user"
    assert user_data["is_active"] is True

    login_response = client.post(
        "/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_login_invalid_credentials() -> None:
    client = TestClient(app)
    response = client.post(
        "/login",
        json={"email": "nonexistent@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
