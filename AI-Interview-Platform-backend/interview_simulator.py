import requests
import json
import websocket
import base64
import sounddevice as sd
import soundfile as sf
import os
import time
import playsound  # For playing TTS audio
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8000"
USER_CREDENTIALS = {"email": "shrouk@gmail.com", "password": "123456"}
INTERVIEW_ID = "f366428a-b867-415f-bc83-faa0f75c6e5c"  # Replace with your interview UUID

def login_user():
    """Log in to get an auth token."""
    signin_url = f"{BASE_URL}/signin"
    headers = {"Content-Type": "application/json", "accept": "application/json"}
    response = requests.post(signin_url, headers=headers, data=json.dumps(USER_CREDENTIALS))
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Logged in as {USER_CREDENTIALS['email']}.")
        return token
    print(f"Login failed: {response.text}")
    return None

def record_audio(duration=30, fs=16000):
    """Record audio from the microphone."""
    print(f"Recording response for {duration} seconds... Speak now!")
    audio_path = f"response_{int(time.time())}.wav"
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(audio_path, audio, fs)
    print(f"Response recorded to {audio_path}")
    return audio_path

def play_tts(tts_path):
    """Play the TTS audio file."""
    if os.path.exists(tts_path):
        print("Playing question...")
        playsound.playsound(tts_path)
        print("Question finished.")
    else:
        print(f"TTS file not found: {tts_path}")

def start_interview(token, interview_id):
    """Simulate a real interview via WebSocket."""
    ws_url = f"ws://127.0.0.1:8000/interviews/{interview_id}/live"
    ws = websocket.WebSocket()
    ws.connect(ws_url, header={"Authorization": f"Bearer {token}"})

    print(f"Connected to interview {interview_id}. Waiting for questions...")

    try:
        while True:
            message = ws.recv()
            data = json.loads(message)
            print(f"Received: {data}")

            if data["type"] == "status":
                print(data["message"])
                if data["message"] == "Interview completed":
                    break

            elif data["type"] == "question":
                print(f"Question {data['index']}: {data['question']}")
                # Fetch TTS audio via REST API (since WebSocket sends question text)
                tts_data = get_tts(token, interview_id)
                if tts_data:
                    tts_path = tts_data["tts_path"]
                    play_tts(tts_path)
                    # Record user response
                    audio_path = record_audio(duration=30)  # 30 seconds per response
                    with open(audio_path, "rb") as f:
                        audio_data = f.read()
                    ws.send(json.dumps({
                        "type": "audio",
                        "data": base64.b64encode(audio_data).decode("utf-8")
                    }))
                    os.remove(audio_path)
                    os.remove(tts_path)

            elif data["type"] == "evaluation":
                print("Evaluation received:")
                eval_data = data["evaluation"]
                print(f"Sentiment: {eval_data.get('sentiment', 'N/A')}")
                print(f"Clarity: {eval_data.get('clarity', 'N/A')}/10")
                print(f"Confidence: {eval_data.get('confidence', 'N/A')}/10")
                print(f"Relevance: {eval_data.get('relevance', 'N/A')}")
                print(f"Summary: {eval_data.get('summary', 'N/A')}")
                print(f"Score: {eval_data.get('score', 'N/A')}/10")

            elif data["type"] == "error":
                print(f"Error: {data['message']}")
                break

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        ws.close()
        print("Interview session ended.")

def get_tts(token, interview_id):
    """Fetch TTS audio for the current question."""
    url = f"{BASE_URL}/interviews/{interview_id}/tts"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers)  # Changed to POST as per main.py
    if response.status_code == 200:
        data = response.json()
        tts_path = f"tts_{interview_id}_{int(time.time())}.mp3"
        with open(tts_path, "wb") as f:
            f.write(base64.b64decode(data['audio']))
        print(f"TTS saved to {tts_path}")
        return {"question": data["question"], "tts_path": tts_path}
    else:
        print(f"Failed to get TTS: {response.text}")
        return None

if __name__ == "__main__":
    token = login_user()
    if token:
        start_interview(token, INTERVIEW_ID)