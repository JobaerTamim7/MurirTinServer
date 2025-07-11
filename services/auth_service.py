from fastapi import HTTPException, status
from database import supabase
from gotrue import AuthResponse
import logging


async def authenticate_user(email: str, password: str):
    try:
        auth_response : AuthResponse  = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not auth_response.session or not auth_response.session.access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "access_token": auth_response.session.access_token, 
            "token_type": "bearer"
        }
        
    except Exception as e:
        logging.error(f"Authentication failed for email {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )