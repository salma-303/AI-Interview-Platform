import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_signup():
    # Test successful user signup
    response = client.post(
        "/signup",
        json={"email": "test@example.com", "password": "password123", "role": "user"}
    )
    assert response.status_code == 200
    assert "message" in response.json()

def test_signup_duplicate_email():
    # Test duplicate email signup
    client.post("/signup", json={"email": "test@example.com", "password": "password123"})
    response = client.post("/signup", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_signin():
    # Test successful user signin
    client.post("/signup", json={"email": "newuser@example.com", "password": "password123"})
    response = client.post("/signin", json={"email": "newuser@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
