# In your FastAPI routers (e.g., routers/profile.py)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from supabase import Client
from database import supabase

router = APIRouter(prefix="/profile", tags=["profile"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.get("/me")
async def get_user_profile(token: str = Depends(oauth2_scheme)):
    try:
        user = supabase.auth.get_user(token)
        user_id = user.user.id
        
    
        response = supabase.table("user_profiles").select("username, email").eq("id", user_id).single().execute()
            
        return response.data
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch profile: {str(e)}"
        )