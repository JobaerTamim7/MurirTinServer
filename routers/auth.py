from fastapi import APIRouter, HTTPException, status, Depends
from database import supabase
from models.user import UserLogin, Token, TokenData
from gotrue import AuthResponse
from utils.jwt_token import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(credentials: UserLogin):
    try:
        auth_response : AuthResponse = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        if auth_response.session is None or auth_response.session.access_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        return {
            "access_token": auth_response.session.access_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

@router.post("/verify")
async def verify_token(current_user: dict = Depends(get_current_user)):
    try:
        return {
            "valid": True,
            "user": current_user,
            "message": "Token is valid"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}"
        )