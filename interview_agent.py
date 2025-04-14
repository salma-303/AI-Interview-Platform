import uuid
import time
import os
import cv2
import sounddevice as sd
import soundfile as sf
from gtts import gTTS
from crewai import Agent
from whisper_module import transcribe_audio_local
from evaluation_agent import evaluate_answer
from logger_agent import log_interview_data, save_transcript
from database import supabase

class InterviewAgent(Agent):
    def __init__(self, candidate_id):
        self.session_id = str(uuid.uuid4())
        self.start_time = time.time()
        self.candidate_id = candidate_id
        self.job_info = self.fetch_job_info()
        self.questions = self.job_info.get("interview_questions", [])
        self.parsed_info = self.job_info.get("parsed_info", {})
        self.job_title = self.job_info.get("job_title", "")
        self.transcript = []

    def fetch_job_info(self):
        response = supabase.table("candidates").select("*", count='exact').eq("id", self.candidate_id).execute()
        if response.data:
            return response.data[0]
        return {}

    def text_to_speech(self, text):
        tts = gTTS(text)
        path = f"tts_question_{uuid.uuid4()}.mp3"
        tts.save(path)
        os.system(f"start {path}" if os.name == 'nt' else f"afplay {path}")  # Windows or macOS
        return path

    def record_audio(self, filename="response.wav", duration=30, fs=16000):
        print("Recording audio...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        sf.write(filename, audio, fs)
        print("Audio recorded.")
        return filename

    def record_video(self, filename="response_video.avi", duration=30):
        print("Recording video...")
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

        start_time = time.time()
        while int(time.time() - start_time) < duration:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
                cv2.imshow('Recording', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print("Video recorded.")
        return filename

    def start_interview(self):
        for question in self.questions:
            print(f"Asking: {question}")
            self.text_to_speech(question)

            video_path = self.record_video(duration=20)
            audio_path = self.record_audio(duration=20)

            answer_text = transcribe_audio_local(audio_path, model_size="base")
            self.transcript.append({"question": question, "answer": answer_text})

            eval_result = evaluate_answer(answer_text, self.job_title, self.parsed_info)
            log_interview_data(self.session_id, self.candidate_id, question, answer_text, eval_result)

        save_transcript(self.session_id, self.candidate_id, self.transcript)
        print("Interview session completed.")
