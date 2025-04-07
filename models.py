# Import BaseModel from Pydantic to create data validation models
from pydantic import BaseModel , EmailStr, validator
# Import Optional from typing to allow fields to be either a type or None
from typing import Optional ,List, Dict
import json

# Define a Pydantic model for user sign-up data
class UserSignUp(BaseModel):
    # Email field, required, must be a string (e.g., "user@example.com")
    email: str
    # Password field, required, must be a string (e.g., "mypassword123")
    password: str
    # Role field, optional, defaults to "user" if not provided, must be a string
    role: str = "user"

# Define a Pydantic model for user sign-in data
class UserSignIn(BaseModel):
    # Email field, required, must be a string
    email: str
    # Password field, required, must be a string
    password: str

# Define a Pydantic model for creating a job posting
class JobCreate(BaseModel):
    # Title field, required, must be a string (e.g., "Software Engineer")
    title: str
    # Brief field, required, must be a string (short job description)
    brief: str
    # Requirements field, required, must be a string (list of job requirements)
    requirements: str
    status: str = "Draft"  # Optional, defaults to "Draft"
class JobUpdate(BaseModel):
    title: Optional[str] = None
    brief: Optional[str] = None
    requirements: Optional[str] = None
    status: Optional[str] = None  # All fields optional for update

class ApplicantRequest(BaseModel):
    user_id: str



    
# Define a Pydantic model for updating a CV with processed data
class CVUpdate(BaseModel):
    applicant_id: Optional[str] = None
    file_url: Optional[str] = None
    processed_data: Optional[dict] = None
    processing_status: Optional[str] = None