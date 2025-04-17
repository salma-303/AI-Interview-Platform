# AI-Interview-Platform
The system automates CV parsing, question generation, response evaluation, and integrates AI to streamline hiring. It features an interactive frontend for candidates and HR, backed by a scalable FastAPI-based backend

**AI Interview Platform Documentation**  

**Installation:**

1 - Use ```git clone https://github.com/salma-303/AI-Interview-Platform```

2 - Install requirments using
```
npm install package.json
pip install -r requirements.txt
```
3 - Run `start.sh`

You can export a docker image by running `dockerize.bat`

**Bugs that need to be resolved**



1- 
```
During an automated interview session, the system recorded the candidate's response inaccurately. Instead of capturing the actual spoken answer, the recorded audio output consisted solely of the repeated word "you", resulting in a failed evaluation.

System Response:

json
CopyEdit

{
  "type": "evaluation",
  "evaluation": {
    "sentiment": "Neutral",
    "clarity": 1,
    "confidence": 1,
    "relevance": "None",
    "summary": "The answer consists entirely of the word 'you' repeated multiple times. It provides no information about the candidate's skills, experience, or thought process. Therefore, it's impossible to extract any meaningful points related to the AI2 position.",
    "score": 1,
    "timestamp": "2025-04-15 21:23:27.229889"
  }
}

Audio Processing Issue: The recorded file (response_1744752201.wav) did not capture the candidate's actual speech and instead contained an audio loop or a corrupted input repeating the word "you".

Evaluation Impact: The system evaluated the response based on the incorrect audio content, resulting in:
- Clarity: 1/10
- Confidence: 1/10
- Relevance: None
- Score: 1/10
```

2 - 
```
Supabase authentication is not aligned with frontend javascript token, which disables log in entirely
You can still run AI-Interview-Platform-backend/client.py to mimic client side
```
3 - 
```
Sign in page is not coordinated with the latest version of database
```
4 - 
```
TTS is running both on server and client sides
```

**1. Overview**  
The AI Interview Platform automates job applications and interviews using AI. It has:  
- Frontend: Streamlit (user interface).  
- Backend: FastAPI (APIs, auth).  
- AI/ML: Gemini (CV analysis), Whisper (speech-to-text), TTS (text-to-speech).  
- Database: Supabase (users, jobs, CVs, interviews).  
- Cloud: AWS (deployment).  

**2. Team Roles**  
- Frontend: Ahmed Atef.  
- Backend: Shrouk.  
- AI/ML: Salma.  
- Testing & QA: Nayra.  
- Deployment & Docs: Ahmed Mostafa.  

**3. GitHub Setup**  
Repo: [github.com/salma-303/AI-Interview-Platform](https://github.com/salma-303/AI-Interview-Platform).  
Branching strategy: Main branch + feature branches.  
Folders:  
- `backend/`: FastAPI (main.py, cv_parser.py, interview_manager.py).  
- `frontend/`: Streamlit (app.py, pages).  
- `database/`: Supabase config.  
- `deployment/`: AWS scripts.  

**4. Workflow (CI/CD)**  
GitHub Actions: Super-Linter runs on push to check code quality.  

**5. Database Schema (Supabase)**  
Tables:  
- `users`: User emails, roles (user/admin).  
- `jobs`: Job titles, descriptions.  
- `applicants`: Links users to jobs.  
- `cvs`: CV files (PDFs → JSON after parsing).  
- `interviews`: Transcripts, scores.  

**6. Authentication**  
- JWT tokens for user sessions.  
- Supabase handles auth (signup/signin).  
- FastAPI validates tokens via `get_current_user()`.  
- Row-Level Security (RLS) enabled (users see only their data).  

**7. Backend APIs (FastAPI)**  
Endpoints:  
- **Auth**: `/signup`, `/signin`.  
- **Jobs**: CRUD (`/jobs`, `/jobs/{id}`).  
- **Applicants**: Apply to jobs (`/jobs/{id}/applicants`).  
- **CVs**: Upload/delete (`/applicants/{id}/cv`).  
- **Interviews**: Start/fetch results (`/interviews/{id}`).  

**8. AI/ML Flow**  
- CV uploaded → FastAPI → parsed to JSON (Gemini) → stored in Supabase.  
- Interview:  
  1. User speaks → Whisper (STT) → text.  
  2. CrewAI generates questions (uses CV JSON).  
  3. AI scores answers → saves to Supabase.  
  4. TTS converts AI replies to audio.  

**9. Frontend (Streamlit)**  
- Pages: Signup, job listings, CV upload, interview.  
- UI: Two screens (will add images later).  

**10. Deployment**  
- AWS: Hosts FastAPI/Streamlit.  
- Supabase: Database + auth.  

**11. Testing**  
- QA: Nayra tests endpoints, AI accuracy.  
- Swagger UI: [localhost:8000/docs](http://localhost:8000/docs) for API tests.  

**12. Tech Stack**  
- Backend: FastAPI (Python).  
- Frontend: Streamlit.  
- AI: Gemini, Whisper, CrewAI.  
- DB: Supabase (PostgreSQL).  
- Cloud: AWS.  

