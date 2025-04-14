from crewai import Agent
from utils.llm import gemini_client

class EvaluationAgent(Agent):
    def __init__(self, name="EvaluationAgent"):
        super().__init__(name)

    def analyze_response(self, transcribed_text: str, job_title: str, parsed_info: dict) -> dict:
        prompt = f"""
        You are an interview evaluation assistant. Analyze the following answer from a candidate for the position of '{job_title}'.
        Candidate background: {parsed_info}

        Response:
        """
        {transcribed_text}
        """

        Perform the following:
        - Sentiment Analysis (Positive/Neutral/Negative)
        - Clarity (Score 1–10)
        - Confidence (Score 1–10)
        - Relevance to job title and candidate experience
        - Summary of key points
        - Rating of answer from 1 to 10 based on quality and match with the job

        Respond in structured JSON format:
        {{
            "sentiment": "...",
            "clarity": ..., 
            "confidence": ..., 
            "relevance": "...",
            "summary": "...",
            "score": ...
        }}
        """

        response = gemini_client.models.generate_content(
            model='gemini-1.5-pro',
            contents=prompt
        )

        try:
            # Gemini sometimes returns code blocks or markdown, strip them
            import json
            text = response.text.strip().strip("`{}\n")
            return json.loads(text)
        except Exception as e:
            return {"error": str(e), "raw_response": response.text}