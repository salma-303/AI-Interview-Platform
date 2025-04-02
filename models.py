# Import BaseModel from Pydantic to create data validation models
from pydantic import BaseModel
# Import Optional from typing to allow fields to be either a type or None
from typing import Optional

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

# Define a Pydantic model for updating a CV with processed data
class CVUpdate(BaseModel):
    # Processed_data field, optional, can be a dictionary or None
    # Defaults to None if not provided; used for JSON-like CV data
    processed_data: Optional[dict] = None