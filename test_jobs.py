import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # Authenticate a test user and return headers with the token
    signup_data = {"email": "admin@example.com", "password": "password123", "role": "admin"}
    client.post("/signup", json=signup_data)
    signin_response = client.post("/signin", json=signup_data)
    token = signin_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_add_job(auth_headers):
    # Test adding a new job
    job_data = {"title": "Software Engineer", "brief": "Develop software solutions", "requirements": "Python, FastAPI"}
    response = client.post("/jobs", json=job_data, headers=auth_headers)
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_get_all_jobs(auth_headers):
    # Test retrieving all jobs
    response = client.get("/jobs", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_job(auth_headers):
    # Test deleting a job
    job_data = {"title": "Temp Job", "brief": "Temporary job", "requirements": "None"}
    add_response = client.post("/jobs", json=job_data, headers=auth_headers)
    job_id = add_response.json()["job_id"]
    delete_response = client.delete(f"/jobs/{job_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    assert "Job deleted successfully" in delete_response.json()["message"]
