# AI-Interview-Platform
The system automates CV parsing, question generation, response evaluation, and integrates AI to streamline hiring. It features an interactive frontend for candidates and HR, backed by a scalable FastAPI-based backend

**AI Interview Platform Documentation**  

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

