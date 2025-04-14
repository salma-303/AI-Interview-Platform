import uuid
import datetime
import asyncio
import numpy as np
import sounddevice as sd
from gtts import gTTS
import os
from whisper_module import stream_transcribe_audio
from evaluation_agent import EvaluationAgent
from logger_agent import LoggerAgent
from database import supabase

class InterviewAgent:
    def __init__(self, applicant_id: str):
        self.applicant_id = applicant_id
        self.interview_id = str(uuid.uuid4())
        self.logger = LoggerAgent(self.interview_id)
        self.evaluator = EvaluationAgent()
        self.current_question_index = 0

        # Fetch applicant data from Supabase
        response = supabase.table("cvs").select("processed_data, interview_questions").eq("applicant_id", applicant_id).execute()
        if not response.data:
            raise Exception("Applicant CV not found")
        job_response = supabase.table("applicants").select("job_id").eq("id", applicant_id).execute()
        if not job_response.data:
            raise Exception("Applicant not found")
        job_id = job_response.data[0]["job_id"]
        job_title_response = supabase.table("jobs").select("title").eq("id", job_id).execute()
        if not job_title_response.data:
            raise Exception("Job not found")

        self.parsed_info = response.data[0]["processed_data"]
        self.questions = response.data[0]["interview_questions"]
        self.job_title = job_title_response.data[0]["title"]

        # Initialize interview record
        supabase.table("interviews").insert({
            "id": self.interview_id,
            "applicant_id": applicant_id,
            "job_id": job_id,
            "status": "Pending",  # Changed from "InProgress" to "Pending"
            "transcripts": [],
            "results": {"evaluations": []}
        }).execute()

    async def start_interview(self, websocket):
        print(f"[InterviewAgent] Starting interview {self.interview_id} for applicant {self.applicant_id}")
        await websocket.send_json({"type": "status", "message": "Interview started"})

        for idx, question in enumerate(self.questions):
            self.current_question_index = idx
            print(f"[InterviewAgent] Asking question {idx + 1}: {question}")

            # Generate TTS and send question
            tts_path = self.text_to_speech(question)
            await websocket.send_json({"type": "question", "question": question, "index": idx + 1})

            # Stream audio and transcribe in real-time
            transcription = await stream_transcribe_audio(websocket)
            if not transcription:
                await websocket.send_json({"type": "error", "message": "No audio received"})
                continue

            self.logger.log_transcript(question, transcription)

            # Evaluate response
            evaluation = self.evaluator.analyze_response(transcription, self.job_title, self.parsed_info)
            self.logger.log_evaluation(evaluation)

            # Send evaluation to client
            await websocket.send_json({"type": "evaluation", "evaluation": evaluation})

        # Save results to Supabase
        self.logger.save_to_database()
        supabase.table("interviews").update({"status": "Completed"}).eq("id", self.interview_id).execute()  # Already correct
        await websocket.send_json({"type": "status", "message": "Interview completed"})
        print(f"[InterviewAgent] Interview {self.interview_id} completed.")

    def text_to_speech(self, text):
        tts = gTTS(text)
        path = f"tts_{self.interview_id}_{uuid.uuid4()}.mp3"
        tts.save(path)
        return path