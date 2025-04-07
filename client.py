import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000"
USER_CREDENTIALS = {"email": "shrouk@gmail.com", "password": "123456"}
JOB_DATA = {"title": "AI", "brief": "AI engineering", "requirements": "python, ML"}
UPDATE_JOB_DATA = {"title": "AI2", "brief": "AI engineering","status":"Open"}
JOB_ID = "96954db7-d4e4-4a6b-8303-69d405f2dfa5"
UPDATE_JOB_ID = "96954db7-d4e4-4a6b-8303-69d405f2dfa5"
APPLICANT_ID = "7c1b15ce-32fe-4c1e-a7a1-21c95762ffd0"  
User_ID = "03c59878-dec6-42c9-8012-b0c707a4daef"
CV_ID = "67d13e8d-a8da-429e-bf57-e87bb0c37df1"
CV_UPDATE_DATA = {"processing_status": "completed"}


def login_user():
    signin_url = f"{BASE_URL}/signin"
    headers = {"Content-Type": "application/json", "accept": "application/json"}
    response = requests.post(signin_url, headers=headers, data=json.dumps(USER_CREDENTIALS))
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Logged in as {USER_CREDENTIALS['email']}. Token: {token[:20]}...")
        return token
    print(f"Login failed: {response.text}")
    return None

######### User Management ########

def get_all_users(token):
    url = f"{BASE_URL}/users"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"All users: {response.text}")
        return response.json()
    else:
        print(f"Failed to get all users: {response.text}")
        return None
    
######### Job Management #########
    
def add_job(token):
    jobs_url = f"{BASE_URL}/jobs"
    headers = {"Content-Type": "application/json", "accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.post(jobs_url, headers=headers, data=json.dumps(JOB_DATA))
    if response.status_code == 200:
        print(f"Job added: {response.text}")
    else:
        print(f"Failed to add job: {response.text}")


    
def delete_job(token, job_id):
    delete_url = f"{BASE_URL}/jobs/{job_id}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.delete(delete_url, headers=headers)
    if response.status_code == 200:
        print(f"Job deleted: {response.text}")
    else:
        print(f"Failed to delete job: {response.text}")

def update_job(token, job_id):
    update_url = f"{BASE_URL}/jobs/{job_id}"
    headers = {"Content-Type": "application/json", "accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.put(update_url, headers=headers, data=json.dumps(UPDATE_JOB_DATA))
    if response.status_code == 200:
        print(f"Job updated: {response.text}")
    else:
        print(f"Failed to update job: {response.text}")

############# Applicant Management ##################

def add_applicant(token, job_id, user_id):
    url = f"{BASE_URL}/jobs/{job_id}/applicants"
    headers = {"Content-Type": "application/json", "accept": "application/json", "Authorization": f"Bearer {token}"}
    data = {"user_id":user_id,"job_id":job_id}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Applicant added: {response.text}")
        return response.json()
    else:
        print(f"Failed to add applicant: {response.text}")
        return None

def delete_applicant(token, job_id, applicant_id):
    url = f"{BASE_URL}/jobs/{job_id}/applicants/{applicant_id}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Applicant deleted: {response.text}")
    else:
        print(f"Failed to delete applicant: {response.text}")
def get_applicant_history(token, applicant_id):
    url = f"{BASE_URL}/applicants/{applicant_id}/history"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Applicant history: {response.text}")
        return response.json()
    else:
        print(f"Failed to get applicant history: {response.text}")
        return None
######### CV Management ########
def add_cv(token, applicant_id, file_path):
    url = f"{BASE_URL}/applicants/{applicant_id}/cv"
    headers = {"Content-Type": "application/json","accept": "application/json","Authorization": f"Bearer {token}"}
    payload = {"file_path": file_path}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("CV uploaded successfully from file path.")
        return response.json()
    else:
        print("Upload failed:", response.text)
        return None
# update cv info
def update_cv(token, applicant_id, cv_id, update_data):
    url = f"{BASE_URL}/applicants/{applicant_id}/cv/{cv_id}"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.put(url, headers=headers, data=json.dumps(update_data))
    if response.status_code == 200:
        print(f"CV updated: {response.text}")
        return response.json()
    else:
        print(f"Failed to update CV: {response.text}")
        return None
    
# delete cv 
def delete_cv(token, applicant_id, cv_id):
    url = f"{BASE_URL}/applicants/{applicant_id}/cv/{cv_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"CV deleted: {response.text}")
        return response.json()
    else:
        print(f"Failed to delete CV: {response.text}")
        return None
######### Interview Management ########

def add_interview(token, applicant_id, job_id):
    url = f"{BASE_URL}/applicants/{applicant_id}/interviews"
    headers = {"Content-Type": "application/json", "accept": "application/json", "Authorization": f"Bearer {token}"}
    data = {"job_id": job_id}  # Only job_id in body since applicant_id is in URL
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"Interview scheduled: {response.text}")
        return response.json()
    else:
        print(f"Failed to schedule interview: {response.text}")
        return None

def get_interview_details(token, interview_id):
    url = f"{BASE_URL}/interviews/{interview_id}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Interview details: {response.text}")
        return response.json()
    else:
        print(f"Failed to get interview details: {response.text}")
        return None

def get_interview_results(token, applicant_id):
    url = f"{BASE_URL}/applicants/{applicant_id}/interviews/results"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Interview results: {response.text}")
        return response.json()
    else:
        print(f"Failed to get interview results: {response.text}")
        return None

##############################################################################

if __name__ == "__main__":
    token = login_user()
    if token:
        #add_job(token)            # Call only if needed
        #delete_job(token, JOB_ID) # Call only if needed
        #update_job(token, UPDATE_JOB_ID)  # New function call
        #add_applicant(token, JOB_ID,User_ID)
        # get_applicant_history(token, APPLICANT_ID)
        #delete_applicant(token ,JOB_ID,APPLICANT_ID)
        # New interview-related calls
        #interview_response = add_interview(token, APPLICANT_ID, JOB_ID)
        #if interview_response:
        #    interview_id = interview_response["interview_id"]
        #    get_interview_details(token, interview_id)
        #get_interview_results(token, APPLICANT_ID)
        # get_all_users(token)
        # add_cv(token, APPLICANT_ID, "a-cv.pdf")
        #update_cv(token,APPLICANT_ID,CV_ID,CV_UPDATE_DATA)
        delete_cv(token,APPLICANT_ID,CV_ID)
        