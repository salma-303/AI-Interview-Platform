from fastapi import FastAPI, Depends, HTTPException, UploadFile, File ,WebSocket
from fastapi.responses import JSONResponse
from supabase import Client
from database import supabase
from models import UserSignUp, UserSignIn, JobCreate,JobUpdate,ApplicantRequest, CVUpdate
from auth import get_current_user #, get_current_admin
import os
# from llm_test import process_cv  # Import LLM processing

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
    users = supabase.table("users").select("id, email, role").execute()
    return users.data

######### Job Management #########
# This section covers APIs for managing job postings, and status tracking.
@app.post("/jobs")
def add_job(job: JobCreate, current_user: dict = Depends(get_current_user)):
    job_data = supabase.table("jobs").insert(job.dict()).execute()
    return {"message": "Job added successfully", "job_id": job_data.data[0]["id"]}

@app.get("/jobs")
def get_all_jobs():
    jobs = supabase.table("jobs").select("*").execute()
    return jobs.data

@app.get("/jobs/{job_id}")
def get_job_details(job_id: str):
    job = supabase.table("jobs").select("*").eq("id", job_id).single().execute()
    if not job.data:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.data

@app.delete("/jobs/{job_id}")
def delete_job(job_id: str, current_user: dict = Depends(get_current_user)):
    supabase.table("jobs").delete().eq("id", job_id).execute()
    return {"message": "Job deleted successfully"}

@app.put("/jobs/{job_id}")
def edit_job(job_id: str, job: JobUpdate, current_user: dict = Depends(get_current_user)):
    job_check = supabase.table("jobs").select("id").eq("id", job_id).execute()
    if not job_check.data:
        raise HTTPException(status_code=404, detail="Job not found")
    update_data = {k: v for k, v in job.dict().items() if v is not None}  # Only include non-None fields
    if not update_data:  # Prevent empty update
        raise HTTPException(status_code=400, detail="No fields provided to update")
    supabase.table("jobs").update(update_data).eq("id", job_id).execute()
    return {"message": "Job updated successfully"}

########## Applicant Management ##################

@app.post("/jobs/{job_id}/applicants")
def add_applicant(job_id: str, request: ApplicantRequest, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin" and current_user["id"] != request.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    applicant_data = supabase.table("applicants").insert({
        "user_id": request.user_id,
        "job_id": job_id
    }).execute()
    return {"message": "Applicant added successfully", "applicant_id": applicant_data.data[0]["id"]}

@app.delete("/jobs/{job_id}/applicants/{applicant_id}")
def delete_applicant(job_id: str, applicant_id: str, current_user: dict = Depends(get_current_user)):
    supabase.table("applicants").delete().eq("id", applicant_id).eq("job_id", job_id).execute()
    return {"message": "Applicant deleted successfully"}

@app.get("/applicants/{applicant_id}/history")
def get_applicant_history(applicant_id: str, current_user: dict = Depends(get_current_user)):
    history = supabase.table("interviews").select("*").eq("applicant_id", applicant_id).execute()
    return history.data

######### CV Management ########

async def add_cv(applicant_id: str, file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    try:
        # Read PDF bytes
        pdf_bytes = await file.read()
        
        # Upload to Supabase Storage
        file_name = f"{applicant_id}_{file.filename}"
        file_path = f"cvs/{file_name}"
        supabase.storage.from_("cvs").upload(file_path, pdf_bytes, file_options={"content-type": "application/pdf"})
        file_url = supabase.storage.from_("cvs").get_public_url(file_path)
        
        # Process PDF with LLM
        processed_data = process_cv(file)
        
        # Insert into cvs table
        cv_data = supabase.table("cvs").insert({
            "applicant_id": applicant_id,
            "file_path": file_url,
            "processed_data": processed_data
        }).execute()
        
        return {
            "message": "CV uploaded successfully",
            "cv_id": cv_data.data[0]["id"],
            "file_path": file_url,
            "processed_data": processed_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload or process CV")

@app.delete("/applicants/{applicant_id}/cv/{cv_id}")
def delete_cv(applicant_id: str, cv_id: str, current_user: dict = Depends(get_current_user)):
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
def add_interview(applicant_id: str, job_id: str, current_user: dict = Depends(get_current_user)):
    interview_data = supabase.table("interviews").insert({"applicant_id": applicant_id, "job_id": job_id}).execute()
    return {"message": "Interview scheduled", "interview_id": interview_data.data[0]["id"]}

@app.get("/interviews/{interview_id}")
def get_interview_details(interview_id: str, current_user: dict = Depends(get_current_user)):
    interview = supabase.table("interviews").select("*").eq("id", interview_id).single().execute()
    if not interview.data:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview.data

@app.get("/applicants/{applicant_id}/interviews/results")
def get_interview_results(applicant_id: str, current_user: dict = Depends(get_current_user)):
    results = supabase.table("interviews").select("results").eq("applicant_id", applicant_id).execute()
    return results.data


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