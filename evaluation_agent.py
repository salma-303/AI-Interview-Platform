import json
from crewai import Agent
from cv import model  # Import Gemini model from cv.py

class EvaluationAgent(Agent):
    def __init__(self, name="EvaluationAgent"):
        super().__init__(
            name=name,
            role="Interview Evaluator",
            goal="Analyze candidate responses for sentiment, clarity, confidence, relevance, and quality.",
            backstory="An AI assistant trained to evaluate interview answers based on job requirements and candidate background."
        )

    def analyze_response(self, transcribed_text: str, job_title: str, parsed_info: dict) -> dict:
        prompt = f"""
        You are an interview evaluation assistant. Analyze the following answer from a candidate for the position of '{job_title}'.
        Candidate background: {json.dumps(parsed_info)}

        Response:
        {transcribed_text}

        Perform the following:
        - Sentiment Analysis (Positive/Neutral/Negative)
        - Clarity (Score 1–10)
        - Confidence (Score 1–10)
        - Relevance to job title and candidate experience
        - Summary of key points
        - Rating of answer from 1 to 10 based on quality and match with the job

        Return in valid JSON format:
        {{
            "sentiment": "...",
            "clarity": ...,
            "confidence": ...,
            "relevance": "...",
            "summary": "...",
            "score": ...
        }}
        """
        try:
            response = model.generate_content(prompt)
            cleaned_text = response.text.strip()
            return json.loads(cleaned_text)
        except Exception as e:
            return {"error": str(e), "raw_response": response.text if response else "No response"}