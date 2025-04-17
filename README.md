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





1- During an automated interview session, the system recorded the candidate's response inaccurately. Instead of capturing the actual spoken answer, the recorded audio output consisted solely of the repeated word "you", resulting in a failed evaluation.

System Response:

json
```

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


2 - Backend Issue: GPU Memory Error during Live Interview API Execution

An error occurred in the **Live Interview API**, traced to the **Whisper model processing audio data** (likely in `whisper_module.py`). The exception raised was:  torch.OutOfMemoryError: CUDA out of memory

**Root Cause**

The error indicates that the **GPU (2GB capacity)** ran out of memory during inference with the **Whisper model**. PyTorch attempted to allocate additional memory (~**3.65GB total**), which **exceeded the physical limits** of the available GPU.


3 - not handling admin part


# Documentation:
**1. Overview**  
The AI Interview Platform automates job applications and interviews using AI. It has:  
- Frontend: HTML , CSS ,Type script.  
- Backend: FastAPI (APIs, auth).  
- AI/ML: Gemini (CV analysis), Whisper (speech-to-text), TTS (text-to-speech).  
- Database: Supabase (users, jobs, CVs, interviews , applicants).  
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
- `backend/`: FastAPI , database , AI files .  
- `frontend/`: HTML , CSS ,Type script files .  
- `deployment/`: AWS scripts.  

**4. Workflow (CI/CD)**  
GitHub Actions: Super-Linter runs on push to check code quality.  

**5. Database Schema (Supabase)**  
Tables:  
---

### `applicants`

**Purpose:**  
Stores information about individuals applying for jobs.

**Description:**  
Links users to specific job applications, tracking who applied for which job and when. Each applicant is uniquely identified and associated with a user and job via foreign keys.

**Key Fields:**
- `id`: Unique identifier for the applicant.  
- `user_id`: References the user applying.  
- `job_id`: References the job applied for.  
- `created_at`: Timestamp of application creation.  

---

### `cvs`

**Purpose:**  
Manages uploaded CVs for applicants, including AI processing details.

**Description:**  
Stores CV file paths, processing status (`pending`, `completed`, or `failed`), extracted data, and AI-generated interview questions. Each CV is linked to an applicant, with a unique file path constraint to prevent duplicates.

**Key Fields:**
- `id`: Unique identifier for the CV.  
- `applicant_id`: References the associated applicant.  
- `file_path`: Location of the uploaded CV file.  
- `processing_status`: Tracks AI processing state.  
- `processed_data`: Stores extracted CV data in JSON format.  
- `interview_questions`: AI-generated questions based on CV.  

---

### `interviews`

**Purpose:**  
Tracks AI-conducted interviews for applicants.

**Description:**  
Records interview details, including status (e.g., `Pending`), results, and transcripts. Each interview is tied to an applicant and job, enabling evaluation of candidate performance.

**Key Fields:**
- `id`: Unique identifier for the interview.  
- `applicant_id`: References the applicant.  
- `job_id`: References the job.  
- `status`: Current state of the interview (e.g., `Pending`).  
- `results`: AI-generated evaluation data in JSON format.  
- `transcripts`: Stores interview transcripts in JSON format.  

---

### `jobs`

**Purpose:**  
Stores job postings created by recruiters.

**Description:**  
Contains job details like title, brief, requirements, and status (e.g., `Draft`). Constraints ensure reasonable length limits for text fields to maintain data quality.

**Key Fields:**
- `id`: Unique identifier for the job.  
- `title`: Job title (max 100 characters).  
- `brief`: Short job description (max 1000 characters).  
- `requirements`: Detailed job requirements (max 2000 characters).  
- `status`: Job posting status (e.g., `Draft`).  

---

### `users`

**Purpose:**  
Manages user accounts for recruiters and applicants.

**Description:**  
Stores user credentials, roles (e.g., `user`, `admin`), and registration timestamps. Email uniqueness and lowercase constraints ensure consistent identification.

**Key Fields:**
- `id`: Unique identifier for the user.  
- `email`: Unique, lowercase email address.  
- `password`: User password.  
- `role`: User role (e.g., `user`, `admin`).  
- `created_at`: Timestamp of user account creation.   

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
- Cloud: GCP.

**13. Frontend Overview**

[Watch the video](./frontend.mp4)
<video src="frontend.mp4" controls width="500"></video>


**14. Backend Documentation**

The system is designed to automate the recruitment process by allowing users to:
- Sign up and sign in using Supabase authentication.
- Create, manage, and apply for job postings.
- Upload and process CVs (PDF format) using Google Gemini for parsing and generating tailored interview questions.
- Conduct live interviews via WebSocket with real-time audio transcription and evaluation.
- Store and manage data (users, jobs, applicants, CVs, interviews) in Supabase.
- Log and evaluate interview responses for sentiment, clarity, confidence, and relevance.

The codebase is modular, with separate files handling specific functionalities such as CV processing, database interactions, interview simulation, and logging.

## File Structure and Purpose
1. **cv.py**: Handles CV processing and interview question generation using Google Gemini.
2. **database.py**: Configures the Supabase client for database and storage operations.
3. **interview_agent.py**: Manages the interview process, including question delivery, audio transcription, and response evaluation.
4. **evaluation_agent.py**: Evaluates candidate responses for sentiment, clarity, confidence, and relevance.
5. **interview_simulator.py**: Simulates a client-side interview experience with audio recording and playback.
6. **logger_agent.py**: Logs interview transcripts, evaluations, and media for storage in Supabase.
7. **models.py**: Defines Pydantic models for data validation (e.g., user signup, job creation).
8. **main.py**: Defines FastAPI routes for user management, job management, CV processing, and live interviews.
9. **auth.py**: Handles user authentication using Supabase JWT tokens.

## Detailed File Documentation

### 1. `cv.py`
**Purpose**: Processes CV files (PDF or DOCX) to extract structured data and generate tailored interview questions using Google Gemini.

**Key Functions**:
- `extract_text_from_pdf(pdf_path)`: Extracts text from a PDF file using pdfplumber.
- `extract_text_from_docx(docx_path)`: Extracts text from a DOCX file using docx2txt.
- `parse_cv_with_gemini(cv_text)`: Uses Google Gemini to parse CV text into structured JSON with fields: name, email, phone, education, experience, skills.
- `process_cv(file_path, file_type="pdf")`: Orchestrates CV text extraction and parsing, ensuring valid JSON output.
- `generate_interview_questions(cv_data, job_title="software developer")`: Generates 5 tailored interview questions based on CV data and job title, focusing on coding skills, data structures, problem-solving, and tools.

**Dependencies**:
- fastapi, google.generativeai, pdfplumber, docx2txt, json, re

**Notes**:
- The Google API key is hardcoded (replace with environment variables in production).
- The system assumes CVs are primarily in PDF format.
- JSON parsing errors are handled with detailed error messages.

### 2. `database.py`
**Purpose**: Initializes the Supabase client for database and storage operations.

**Key Components**:
- Constants:
  - `SUPABASE_URL`: Supabase project URL.
  - `SUPABASE_KEY`: Anonymous API key for public access.
- Client:
  - `supabase`: A Client instance created using `create_client(SUPABASE_URL, SUPABASE_KEY)`.

**Dependencies**:
- supabase

**Notes**:
- The anon key is hardcoded (use environment variables in production).
- The client is used across other modules for database operations (e.g., users, jobs, cvs, interviews tables).

### 3. `interview_agent.py`
**Purpose**: Manages the live interview process, including question delivery, audio transcription, response evaluation, and logging.

**Key Components**:
- **Class**: `InterviewAgent`
  - Attributes:
    - `applicant_id`: Unique identifier for the applicant.
    - `interview_id`: Unique identifier for the interview (generated if not provided).
    - `logger`: `LoggerAgent` instance for logging transcripts and evaluations.
    - `evaluator`: `EvaluationAgent` instance for analyzing responses.
    - `questions`: List of interview questions fetched from the `cvs` table.
    - `parsed_info`: Processed CV data from the `cvs` table.
    - `job_title`: Job title associated with the applicant’s job application.
  - Methods:
    - `__init__(applicant_id, interview_id)`: Initializes the agent, fetches applicant data, and creates an interview record in Supabase.
    - `start_interview(websocket)`: Runs the interview loop, sending questions, streaming audio, transcribing responses, evaluating answers, and logging results.
    - `text_to_speech(text)`: Generates TTS audio for questions using gTTS.

**Dependencies**:
- uuid, datetime, asyncio, numpy, sounddevice, gtts, whisper_module, evaluation_agent, logger_agent, database

**Notes**:
- Uses WebSocket for real-time communication with the client.
- Assumes the `whisper_module` (not provided) handles audio transcription.
- Interview status is updated to `Completed` upon finishing.

### 4. `evaluation_agent.py`
**Purpose**: Analyzes candidate responses during interviews using Google Gemini.

**Key Components**:
- **Class**: `EvaluationAgent` (inherits from `crewai.Agent`)
  - Attributes:
    - `name`: Agent name (`EvaluationAgent`).
    - `role`: Role description (`Interview Evaluator`).
    - `goal`: Objective



