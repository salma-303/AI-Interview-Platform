from fastapi import FastAPI, Depends, HTTPException, UploadFile, File ,WebSocket ,Body
from fastapi.responses import JSONResponse
import json
from supabase import Client
from database import supabase
from models import UserSignUp, UserSignIn, JobCreate,JobUpdate,ApplicantRequest, CVUpdate 
from auth import get_current_user #, get_current_admin
import os
from cv import process_cv , generate_interview_questions # Import cv processing functions
from interview_manager import transcribe_audio_local, process_response_with_gemini
app = FastAPI()

# Set up the FastAPI app with authentication endpoints
# This module defines routes for user signup and signin, integrating with Supabase for authentication.

@app.post("/signup")
def signup(user: UserSignUp):
    # Define the signup endpoint to register a new user.
    # Expects a UserSignUp object (Pydantic model) with fields like email, password, and role.
    try:
        # Sign up user with Supabase Auth
        # Calls Supabase's sign_up method to create a new user in the auth system.
        # Returns an auth response containing user details and session info.
        auth_response = supabase.auth.sign_up({"email": user.email, "password": user.password})
        
        # Insert user into users table
        # After successful auth signup, store additional user data in a custom 'users' table.
        # Note: 'id' is taken from auth_response to link auth user with database record.
        supabase.table("users").insert({
            "id": auth_response.user.id,  # Unique user ID from Supabase Auth
            "email": user.email,          # User's email address
            "password": user.password,    # In practice, hash this (plaintext storage is insecure)
            "role": user.role             # User role (e.g., 'admin', 'user') from UserSignUp model
        }).execute()
        
        # Return success message
        # Indicates the user was created successfully in both auth and database.
        return {"message": "User created successfully"}
    
    except Exception as e:
        # Handle any errors during signup (e.g., duplicate email, Supabase errors)
        # Raises a 400 Bad Request with the error message for debugging or user feedback.
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/signin")
def signin(user: UserSignIn):
    # Define the signin endpoint to authenticate an existing user.
    # Expects a UserSignIn object (Pydantic model) with email and password fields.
    try:
        # Authenticate user with Supabase Auth
        # Uses Supabase's sign_in_with_password to verify credentials and generate a session.
        # Returns an auth response with an access token if successful.
        auth_response = supabase.auth.sign_in_with_password({"email": user.email, "password": user.password})
        
        # Return access token
        # Sends the JWT access token and token type to the client for use in authenticated requests.
        return {"access_token": auth_response.session.access_token, "token_type": "bearer"}
    
    except Exception as e:
        # Log error for debugging
        # Prints the error type and message (e.g., AuthApiError: Email not confirmed) to server logs.
        print(f"Sign-in failed: {type(e).__name__}: {str(e)}")
        
        # Handle authentication failure
        # Raises a 401 Unauthorized error with a generic message for the client.
        # Note: Could be refined to distinguish between "email not confirmed" and "wrong credentials".
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.get("/users")
def get_all_users(current_user: dict = Depends(get_current_user)):
    # Retrieve a list of all users from the 'users' table.
    # Requires authentication via get_current_user dependency to ensure only authorized users can access.
    # Returns a list of user objects with id, email, and role fields.
    users = supabase.table("users").select("id, email, role").execute()
    return users.data

######### Job Management #########
# This section covers APIs for managing job postings, and status tracking.
@app.post("/jobs")
def add_job(job: JobCreate, current_user: dict = Depends(get_current_user)):
    # Create a new job posting in the 'jobs' table.
    # Expects a JobCreate object (Pydantic model) with fields like title, brief, and requirements.
    # Requires authentication to ensure only authorized users (e.g., admins) can add jobs.
    job_data = supabase.table("jobs").insert(job.dict()).execute()
    return {"message": "Job added successfully", "job_id": job_data.data[0]["id"]}

@app.get("/jobs")
def get_all_jobs():
    # Retrieve a list of all job postings from the 'jobs' table.
    jobs = supabase.table("jobs").select("*").execute()
    return jobs.data

@app.get("/jobs/{job_id}")
def get_job_details(job_id: str):
    # Retrieve details of a specific job by its ID.
    job = supabase.table("jobs").select("*").eq("id", job_id).single().execute()
    if not job.data:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.data

@app.delete("/jobs/{job_id}")
def delete_job(job_id: str, current_user: dict = Depends(get_current_user)):
    # Delete a specific job by its ID from the 'jobs' table.
    supabase.table("jobs").delete().eq("id", job_id).execute()
    return {"message": "Job deleted successfully"}

@app.put("/jobs/{job_id}")
def edit_job(job_id: str, job: JobUpdate, current_user: dict = Depends(get_current_user)):
    # Update details of a specific job by its ID.
    # Expects a JobUpdate object (Pydantic model) with optional fields to update (e.g., title, status).
    job_check = supabase.table("jobs").select("id").eq("id", job_id).execute()
    if not job_check.data:
        raise HTTPException(status_code=404, detail="Job not found")
    update_data = {k: v for k, v in job.dict().items() if v is not None}  # Only include non-None fields
    if not update_data:  # Prevent empty update
        raise HTTPException(status_code=400, detail="No fields provided to update")
    supabase.table("jobs").update(update_data).eq("id", job_id).execute()
    return {"message": "Job updated successfully"}

############# Applicant Management ##################

@app.post("/jobs/{job_id}/applicants")
def add_applicant(job_id: str, request: ApplicantRequest, current_user: dict = Depends(get_current_user)):
    # Add an applicant to a specific job in the 'applicants' table.
    # Expects an ApplicantRequest object with user_id to link a user to a job.
    if current_user["role"] != "admin" and current_user["id"] != request.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    applicant_data = supabase.table("applicants").insert({
        "user_id": request.user_id,
        "job_id": job_id
    }).execute()
    return {"message": "Applicant added successfully", "applicant_id": applicant_data.data[0]["id"]}

@app.delete("/jobs/{job_id}/applicants/{applicant_id}")
def delete_applicant(job_id: str, applicant_id: str, current_user: dict = Depends(get_current_user)):
    # Remove an applicant from a specific job in the 'applicants' table.
    supabase.table("applicants").delete().eq("id", applicant_id).eq("job_id", job_id).execute()
    return {"message": "Applicant deleted successfully"}

@app.get("/applicants/{applicant_id}/history")
def get_applicant_history(applicant_id: str, current_user: dict = Depends(get_current_user)):
    # Retrieve the interview history for a specific applicant from the 'interviews' table.
    history = supabase.table("interviews").select("*").eq("applicant_id", applicant_id).execute()
    return history.data

######### CV Management ########

@app.post("/applicants/{applicant_id}/cv")
def add_cv_from_path(
    applicant_id: str,
    file_path: str = Body(..., embed=True),  # Accepts JSON body like {"file_path": "path/to/file.pdf"}
    current_user: dict = Depends(get_current_user)
):
    # Upload and process a CV file for an applicant, storing it in Supabase Storage and metadata in 'cvs' table.
    # Expects a JSON body with a 'file_path' field pointing to a local PDF file.
    # Requires authentication to link the CV to an authorized applicant.
    # Validate path
    if not os.path.isfile(file_path) or not file_path.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid PDF file path")

    try:
        # Read file contents from disk
        with open(file_path, "rb") as f:
            file_contents = f.read()

        # Process file (reuse your existing logic)
        processed_data = process_cv(file_path, file_type="pdf")

        # Fetch job title from applicants and jobs tables
        applicant = supabase.table("applicants").select("job_id").eq("id", applicant_id).execute()
        if not applicant.data:
            raise HTTPException(status_code=404, detail="Applicant not found")
        
        job_id = applicant.data[0]["job_id"]
        job = supabase.table("jobs").select("title").eq("id", job_id).execute()
        if not job.data:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_title = job.data[0]["title"]

        # Generate interview questions
        interview_questions = generate_interview_questions(processed_data, job_title=job_title)

        # Generate unique file name and upload to Supabase
        file_name = f"{applicant_id}_{os.urandom(8).hex()}.pdf"
        remote_path = f"cvs/{file_name}"

        supabase.storage.from_("cvs").upload(
            remote_path, file_contents, file_options={"content-type": "application/pdf"}
        )
        file_url = supabase.storage.from_("cvs").get_public_url(remote_path)
        
        # Save metadata to DB
        cv_data = supabase.table("cvs").insert({
            "applicant_id": applicant_id,
            "file_path": str(file_url),
            "processed_data": processed_data,
            "interview_questions": interview_questions  # Store questions in JSONB column
        }).execute()

        return {
            "message": "CV uploaded successfully from path",
            "cv_id": cv_data.data[0]["id"],
            "file_path": file_url,
            "processed_data": processed_data ,
            "interview_questions": interview_questions
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse CV data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")


@app.delete("/applicants/{applicant_id}/cv/{cv_id}")
def delete_cv(applicant_id: str, cv_id: str, current_user: dict = Depends(get_current_user)):
    # Delete a specific CV by its ID, removing it from both Supabase Storage and the 'cvs' table.
    try:
        cv = supabase.table("cvs").select("file_path").eq("id", cv_id).single().execute()
        if not cv.data:
            raise HTTPException(status_code=404, detail="CV not found")
        
        file_path = cv.data["file_path"].split("/storage/v1/object/public/")[-1]
        supabase.storage.from_("cvs").remove([file_path])
        
        supabase.table("cvs").delete().eq("id", cv_id).execute()
        return {"message": "CV deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete CV")

@app.put("/applicants/{applicant_id}/cv/{cv_id}")
def edit_cv(applicant_id: str, cv_id: str, cv_update: CVUpdate, current_user: dict = Depends(get_current_user)):
    # Update details of a specific CV by its ID in the 'cvs' table.
    try:
        cv = supabase.table("cvs").select("id").eq("id", cv_id).single().execute()
        if not cv.data:
            raise HTTPException(status_code=404, detail="CV not found")
        
        update_data = {k: v for k, v in cv_update.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided to update")
        
        supabase.table("cvs").update(update_data).eq("id", cv_id).execute()
        return {"message": "CV details updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update CV")
    

######## Interview Management #########

@app.post("/applicants/{applicant_id}/interviews")
def add_interview(applicant_id: str, job_id: str = Body(...), current_user: dict = Depends(get_current_user)):
    # Schedule a new interview for an applicant and job in the 'interviews' table.
    interview_data = supabase.table("interviews").insert({"applicant_id": applicant_id, "job_id": job_id}).execute()
    return {"message": "Interview scheduled", "interview_id": interview_data.data[0]["id"]}

@app.get("/interviews/{interview_id}")
def get_interview_details(interview_id: str, current_user: dict = Depends(get_current_user)):
    # Retrieve details of a specific interview by its ID from the 'interviews' table.
    interview = supabase.table("interviews").select("*").eq("id", interview_id).single().execute()
    if not interview.data:
        raise HTTPException(status_code=404, detail="Interview not found")
    job = supabase.table("jobs").select("title, brief").eq("id", interview.data["job_id"]).single().execute()
    # Retrieve applicant details
    applicant = supabase.table("applicants").select("user_id").eq("id", interview.data["applicant_id"]).maybe_single().execute()
    if not applicant.data:
        raise HTTPException(status_code=404, detail="Applicant not found")

    # Retrieve user email
    user = supabase.table("users").select("email").eq("id", applicant.data["user_id"]).maybe_single().execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="User not found")    
    return {
        "interview_id": interview.data["id"],
        "job": job.data,
        "applicant_email": user.data["email"],
        "results": interview.data["results"]
    }

@app.get("/applicants/{applicant_id}/interviews/results")
def get_interview_results(applicant_id: str, current_user: dict = Depends(get_current_user)):
    # Retrieve interview results for a specific applicant from the 'interviews' table.
    results = supabase.table("interviews").select("results").eq("applicant_id", applicant_id).execute()
    return results.data

# test audio 
@app.post("/interviews/{interview_id}/audio-test")
async def test_interview_audio(
    interview_id: str,
    audio: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Test audio processing with Whisper and Gemini without saving to database."""
    try:
        # Save uploaded audio temporarily
        audio_path = f"temp_{interview_id}_{audio.filename}"
        with open(audio_path, "wb") as f:
            f.write(await audio.read())
        
        # Transcribe audio using Whisper
        transcribed_text = transcribe_audio_local(audio_path, model_size="base")
        
        # Process transcription with Gemini
        ai_analysis = process_response_with_gemini(transcribed_text)
        
        # Clean up temporary file
        os.remove(audio_path)
        
        return {
            "message": "Audio processed successfully",
            "interview_id": interview_id,
            "transcription": transcribed_text,
            "ai_analysis": ai_analysis
        }
    except Exception as e:
        # Clean up in case of failure
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")
    
###### TTS/STT and AI Agent Communication ######
@app.websocket("/interview/{interview_id}")
async def interview_websocket(websocket: WebSocket, interview_id: str, token: str = None):
    # Accept connection
    await websocket.accept()
    
    # Validate token (manually, since Depends doesn't work directly with WebSocket)
    if not token:
        await websocket.close(code=1008, reason="Authentication required")
        return
    
    try:
        user = supabase.auth.get_user(token.split("Bearer ")[1] if token.startswith("Bearer ") else token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        current_user = supabase.table("users").select("*").eq("id", user.user.id).single().execute().data
    except Exception:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    print(f"User {current_user['email']} connected to interview {interview_id}")
    
    while True:
        try:
            data = await websocket.receive_text()
            response = {"text": f"Processed response to: {data}"}  # Placeholder
            await websocket.send_json(response)
        except Exception as e:
            print(f"WebSocket error: {str(e)}")
            await websocket.close()
            break