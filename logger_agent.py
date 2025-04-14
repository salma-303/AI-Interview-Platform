import uuid
import datetime
from database import supabase

class LoggerAgent:
    def __init__(self, interview_id: str = None):
        self.interview_id = interview_id or str(uuid.uuid4())
        self.session_data = {
            "interview_id": self.interview_id,
            "start_time": str(datetime.datetime.utcnow()),
            "transcripts": [],
            "evaluations": [],
            "media": [],
        }

    def log_transcript(self, question: str, answer_text: str):
        entry = {
            "question": question,
            "answer": answer_text,
            "timestamp": str(datetime.datetime.utcnow())
        }
        self.session_data["transcripts"].append(entry)

    def log_evaluation(self, evaluation: dict):
        evaluation["timestamp"] = str(datetime.datetime.utcnow())
        self.session_data["evaluations"].append(evaluation)

    def log_media_file(self, file_type: str, file_url: str):
        self.session_data["media"].append({
            "type": file_type,  # e.g., "audio", "video"
            "url": file_url,
            "timestamp": str(datetime.datetime.utcnow())
        })

    def generate_interview_summary(self):
        summary = {
            "interview_id": self.interview_id,
            "summary": "This interview consisted of the following Q&A and evaluation results.",
            "questions_answers": self.session_data["transcripts"],
            "evaluations": self.session_data["evaluations"]
        }
        return summary

    def save_to_database(self):
        try:
            # Save interview session meta info
            supabase.table("interview_sessions").insert({
                "interview_id": self.interview_id,
                "start_time": self.session_data["start_time"],
                "media": self.session_data["media"]
            }).execute()

            # Save transcripts
            for transcript in self.session_data["transcripts"]:
                supabase.table("interview_transcripts").insert({
                    "interview_id": self.interview_id,
                    "question": transcript["question"],
                    "answer": transcript["answer"],
                    "timestamp": transcript["timestamp"]
                }).execute()

            # Save evaluations
            for eval_result in self.session_data["evaluations"]:
                supabase.table("interview_evaluations").insert({
                    "interview_id": self.interview_id,
                    **eval_result
                }).execute()

            # Save final summary
            summary = self.generate_interview_summary()
            supabase.table("interview_summaries").insert({
                "interview_id": self.interview_id,
                "summary": summary
            }).execute()

            print(f"[LoggerAgent] Data saved for interview: {self.interview_id}")

        except Exception as e:
            print(f"[LoggerAgent] Error saving to database: {e}")
