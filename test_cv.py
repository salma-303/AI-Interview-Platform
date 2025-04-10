import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # Authenticate a test user and return headers with the token
    signup_data = {"email": "cvuser@example.com", "password": "password123", "role": "user"}
    client.post("/signup", json=signup_data)
    signin_response = client.post("/signin", json=signup_data)
    token = signin_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_upload_cv(auth_headers, tmp_path):
    # Create a temporary PDF file for testing
    pdf_file = tmp_path / "test_cv.pdf"
    pdf_file.write_text("Sample CV content")
    
    # Test uploading the CV
    response = client.post(
        "/applicants/1/cv",
        json={"file_path": str(pdf_file)},  # Pass the file path as JSON
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "cv_id" in response.json()

def test_invalid_cv_upload(auth_headers, tmp_path):
    # Create a non-PDF file for testing
    invalid_file = tmp_path / "invalid.txt"
    invalid_file.write_text("Invalid file")
    
    # Test uploading an invalid file
    response = client.post(
        "/applicants/1/cv",
        json={"file_path": str(invalid_file)},
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "Invalid PDF file path" in response.json()["detail"]
