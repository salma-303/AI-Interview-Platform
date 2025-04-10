import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # Authenticate a test user and return headers with the token
    signup_data = {"email": "interviewuser@example.com", "password": "password123", "role": "user"}
    client.post("/signup", json=signup_data)
    signin_response = client.post("/signin", json=signup_data)
    token = signin_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_add_interview(auth_headers):
    # Test scheduling an interview
    response = client.post(
        "/applicants/1/interviews",
        json={"job_id": "test-job-id"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "interview_id" in response.json()

def test_process_audio(auth_headers, tmp_path):
    # Create a temporary audio file for testing
    audio_file = tmp_path / "test_audio.wav"
    audio_file.write_bytes(b"fake audio data")
    # Test processing audio
    with open(audio_file, "rb") as f:
        response = client.post(
            "/interviews/1/audio-test",
            files={"audio": ("test_audio.wav", f, "audio/wav")},
            headers=auth_headers
        )
    assert response.status_code == 200
    assert "transcription" in response.json()
