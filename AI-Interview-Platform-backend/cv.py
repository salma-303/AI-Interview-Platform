from fastapi import FastAPI, UploadFile, File
import google.generativeai as genai
import pdfplumber
import docx2txt
import os
from pathlib import Path
import json

# app = FastAPI()

# Configure the API key (hardcoded for simplicity; use env vars in production)
GOOGLE_API_KEY = "GOOGLE_API_KEY"  # Replace or use os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Extract text from DOCX
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

# Use Gemini API for CV parsing
import re

def parse_cv_with_gemini(cv_text):
    prompt = f"""
        Extract key details from the following CV and return structured JSON output **only valid JSON**, without markdown or code formatting.
        CV Text: {cv_text}

        Return JSON with keys: "name", "email", "phone", "education", "experience", "skills".
        """
    response = model.generate_content(prompt)
    try:
        # Extract only the JSON object, discarding any trailing data
        cleaned_text = re.sub(r"(?s)^.*?({.*}).*$", r"\1", response.text.strip())
        parsed_json = json.loads(cleaned_text)
        return parsed_json
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini API returned invalid JSON:\n{response.text}")
    
# Main function to process CV
def process_cv(file_path, file_type="pdf"):
    text = extract_text_from_pdf(file_path) if file_type == "pdf" else extract_text_from_docx(file_path)
    cv_data = parse_cv_with_gemini(text)
    json_string = json.dumps(cv_data)
    # Parse back to ensure validity
    parsed_data = json.loads(json_string)
    print("Valid JSON parsed successfully!")
    return parsed_data


# Generate interview questions based on processed CV
def generate_interview_questions(cv_data, job_title="software developer"):
    """
    Generate customized interview questions based on parsed CV data.
    
    Args:
        cv_data (dict): Parsed CV data with keys: name, skills, education
        job_title (str): Target job title (default: software developer)
    
    Returns:
        list: List of interview questions as strings
    """
    name = cv_data.get("name", "the candidate")
    skills = ", ".join(cv_data.get("skills", [])) if isinstance(cv_data.get("skills"), list) else cv_data.get("skills", "")
    education = json.dumps(cv_data.get("education", [])) if isinstance(cv_data.get("education"), list) else cv_data.get("education", "")

    prompt = f"""
    You are an AI interviewer.

    Based on the candidate's name: {name},
    skills: {skills},
    and education: {education},
    
    generate 5 customized interview questions tailored for a {job_title} role.

    Focus on:
    - practical coding skills
    - data structures
    - problem solving
    - tools or libraries mentioned in the CV

    Return the questions as a JSON array of strings, e.g., ["question 1", "question 2", ...].
    """
    try:
        response = model.generate_content(prompt)
        # Clean and parse the response to ensure valid JSON
        cleaned_text = re.sub(r"(?s)^.*?(\[.*\]).*$", r"\1", response.text.strip())
        questions = json.loads(cleaned_text)
        if not isinstance(questions, list):
            raise ValueError("Expected a list of questions")
        return questions
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Failed to generate questions: {str(e)}\nRaw response: {response.text}")

# Example usage
#cv_data = process_cv("a-cv.pdf", file_type="pdf")
#print(cv_data)
#questions = generate_interview_questions(cv_data)
#print(questions)

