
from fastapi import HTTPException, status
from supabase import Client
from database import supabase
from utils.jwt_token import create_access_token

async def authenticate_user(email: str, password: str):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        return {
            "access_token": auth_response.session.access_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )