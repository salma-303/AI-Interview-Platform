from fastapi import HTTPException, Request, Depends
from supabase import Client
from database import supabase

# Function to authenticate and retrieve the current user's data
async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = token.split(" ")[1]
    try:
        user = supabase.auth.get_user(token)
        user_data = supabase.table("users").select("*").eq("id", user.user.id).single().execute()
        return user_data.data
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# Commented out admin function since admin features are planned for the future
# async def get_current_admin(current_user: dict = Depends(get_current_user)):
#     if current_user["role"] != "admin":
#         raise HTTPException(status_code=403, detail="Not authorized")
#     return current_user