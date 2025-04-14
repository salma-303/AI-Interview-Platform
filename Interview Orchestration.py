import uuid
import datetime
from whisper_module import transcribe_audio_local
from tts_module import speak_text
from audio_video_handler import record_audio_video
from evaluation_agent import EvaluationAgent
from logger_agent import LoggerAgent
from database import supabase

class InterviewAgent:
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id
        self.interview_id = str(uuid.uuid4())
        self.logger = LoggerAgent(self.interview_id)
        self.evaluator = EvaluationAgent()

        # Fetch candidate data from Supabase
        response = supabase.table("candidates").select("parsed_info, interview_questions, job_title").eq("id", self.candidate_id).execute()
        data = response.data[0] if response.data else None
        if not data:
            raise Exception("Candidate not found in database")

        self.parsed_info = data["parsed_info"]
        self.questions = data["interview_questions"]
        self.job_title = data["job_title"]

    def run_interview(self):
        print(f"[InterviewAgent] Starting interview with candidate {self.candidate_id} for {self.job_title}")

        for idx, question in enumerate(self.questions):
            print(f"[InterviewAgent] Asking question {idx + 1}: {question}")

            # TTS
            speak_text(question)

            # Record audio & video
            audio_path, video_path = record_audio_video(duration=30, filename_prefix=f"q{idx + 1}_{self.interview_id}")

            # Log video/audio files
            self.logger.log_media_file("audio", audio_path)
            self.logger.log_media_file("video", video_path)

            # Whisper Transcription
            answer_text = transcribe_audio_local(audio_path)
            self.logger.log_transcript(question, answer_text)

            # Evaluation
            evaluation = self.evaluator.evaluate_response(answer_text, self.parsed_info, self.job_title)
            self.logger.log_evaluation(evaluation)

        # Wrap-up and save all
        self.logger.save_to_database()
        print(f"[InterviewAgent] Interview {self.interview_id} completed and saved.")

# To run the interview session
if __name__ == "__main__":
    candidate_id = "your_candidate_uuid_here"  # Replace with actual candidate UUID
    agent = InterviewAgent(candidate_id)
    agent.run_interview()
