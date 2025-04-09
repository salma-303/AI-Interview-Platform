from supabase import create_client, Client
import json
import os
import pdfplumber
import docx2txt
import requests
import google.generativeai as genai

# === Supabase Setup ===
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# === Gemini API Setup ===
genai.api_key = os.getenv("GEMINI_API_KEY")
client = genai.GenAIModel("google/generativeai")


# === Instructions ===
'''
Before using this module, make sure to configure Supabase and Gemini API credentials.
Ensure you have allowed public access to the cvs bucket in Supabase Storage Policies.

'''


# === Download CV from Supabase ===
def download_cv_from_supabase(cv_url, local_filename="temp_cv"):
    response = requests.get(cv_url)
    if response.status_code != 200:
        return {"error": f"Failed to download CV: {response.status_code}"}
    
    cv_url_lower = cv_url.lower()
    if cv_url_lower.endswith(".pdf"):
        ext = ".pdf"
    elif cv_url_lower.endswith(".docx"):
        ext = ".docx"
    filepath = local_filename + ext

    with open(filepath, "wb") as f:
        f.write(response.content)
    
    return {"filepath": filepath, "file_type": "pdf" if ext == ".pdf" else "docx"}


# === Extract text from PDF ===
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# === Extract text from DOCX ===
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path).strip()

# === Use Gemini API to parse CV ===
def parse_cv_with_gemini(cv_text):
    prompt = f"""
    Extract the following key details from this CV:
    - name
    - email
    - phone
    - education
    - experience
    - skills

    Return a JSON object with the keys:
    {{
      "name": "...",
      "email": "...",
      "phone": "...",
      "education": [...],
      "experience": [...],
      "skills": [...]
    }}

    CV Text:
    {cv_text}
    """
    response = client.models.generate_content(
        model='gemini-1.5-pro-latest',
        contents=prompt)
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw": response.text}


# === Extract and Parse CV ===
def process_cv(file_path, file_type="pdf"):
    text = extract_text_from_pdf(file_path) if file_type == "pdf" else extract_text_from_docx(file_path)
    parsed_data = parse_cv_with_gemini(text)
    return parsed_data

# === Save parsed info to Supabase ===
def save_parsed_info_to_supabase(candidate_id, parsed_info):
    response = supabase.table("candidates").update({"parsed_info": json.dumps(parsed_info)}).eq("id", candidate_id).execute()
    if response.error:
        return {"error": response.error}
    return parsed_info


# === Generate interview questions using extracted info ===
def generate_interview_questions(candidate_data):
    name = candidate_data.get("name", "the candidate")
    skills = ", ".join(candidate_data.get("skills", []))
    education = candidate_data.get("education", [])
    job_title = candidate_data.get("job_title", "software developer")

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
    """
    response = client.models.generate_content(
    model='gemini-1.5-pro-latest',
    contents=prompt)
    return response.text.strip()

# === Load candidate info from Supabase and generate questions ===
def generate_questions_from_supabase(candidate_id):
    # Fetch candidate by ID
    response = supabase.table("candidates").select("*").eq("id", candidate_id).execute()
    if not response.data or len(response.data) == 0:
        return {"error": "Candidate not found"}

    candidate = response.data[0]
    
    # Ensure structured fields
    try:
        parsed_info = json.loads(candidate["parsed_info"]) if isinstance(candidate["parsed_info"], str) else candidate["parsed_info"]
    except Exception:
        return {"error": "Invalid JSON in parsed_info"}

    parsed_info["job_title"] = candidate.get("job_title", "software developer")

    # Generate questions
    questions = generate_interview_questions(parsed_info)
    
    return {
        "parsed_info": parsed_info,
        "interview_questions": questions
    }

# === Save generated questions to Supabase ===
def save_questions_to_supabase(candidate_id, questions_text):
    response = supabase.table("candidates").update({
        "interview_questions": questions_text
    }).eq("id", candidate_id).execute()
    
    if response.error:
        return {"error": response.error}
    return {"message": "Interview questions saved successfully"}

# === Main function ===
def main():
    def main(candidate_id: str):
        """
        Complete CV processing pipeline:
        1. Fetch candidate data from Supabase
        2. Download CV file from storage
        3. Extract text from CV (PDF/DOCX)
        4. Parse CV text with Gemini AI
        5. Save parsed info to Supabase
        6. Generate interview questions based on parsed data
        7. Save questions to Supabase
        
        Args:
            candidate_id: ID of candidate in Supabase database
            
        Returns:
            Dictionary with processing results or error message
        """
        try:
            # 1. Fetch candidate data
            candidate_res = supabase.table("candidates").select(
                "id, cv_url, job_title"
            ).eq("id", candidate_id).execute()
            
            if not candidate_res.data:
                return {"error": f"Candidate {candidate_id} not found"}
                
            candidate = candidate_res.data[0]
            cv_url = candidate.get("cv_url")
            job_title = candidate.get("job_title", "software developer")

            if not cv_url:
                return {"error": "No CV URL found for candidate"}

            # 2. Download CV
            download_res = download_cv_from_supabase(cv_url)
            if "error" in download_res:
                return download_res
                
            filepath = download_res["filepath"]
            file_type = download_res["file_type"]

            # 3. Extract text from CV
            try:
                if file_type == "pdf":
                    text = extract_text_from_pdf(filepath)
                else:
                    text = extract_text_from_docx(filepath)
            except Exception as e:
                return {"error": f"Text extraction failed: {str(e)}"}
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)  # Cleanup temp file

            # 4. Parse CV with Gemini
            parsed_info = parse_cv_with_gemini(text)
            if "error" in parsed_info:
                return parsed_info

            # 5. Save parsed info
            save_res = save_parsed_info_to_supabase(candidate_id, parsed_info)
            if "error" in save_res:
                return save_res

            # 6. Generate interview questions
            candidate_data = {**parsed_info, "job_title": job_title}
            questions = generate_interview_questions(candidate_data)

            # 7. Save questions
            save_q_res = save_questions_to_supabase(candidate_id, questions)
            if "error" in save_q_res:
                return save_q_res

            return {
                "success": True,
                "candidate_id": candidate_id,
                "parsed_info": parsed_info,
                "interview_questions": questions
            }

        except Exception as e:
            return {"error": f"Processing pipeline failed: {str(e)}"}
        

if __name__ == "__main__":
    main()

    # Test the main function with a sample candidate ID
    # result = main("candidate-uuid-1234")
    # if "error" in result:
    #     print(f"Error: {result['error']}")
    # else:
    #     print(f"Generated {len(result['interview_questions'])} questions!")
