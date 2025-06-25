from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer


from database import supabase 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
       

       
        user_response = supabase.auth.get_user(token)

        if not user_response or not user_response.user:
            raise credentials_exception
        
        user = user_response.user

        
        print(f"Supabase user object retrieved successfully: {user.id}")
        print(f"User email: {user.email}")
        print(f"User metadata: {user.user_metadata}")
        
        return {
            "sub": user.id,
            "email": user.email,
            "username": user.user_metadata.get("username")
            }
    except Exception as e:
        if "Invalid JWT" in str(e) or "expired" in str(e): 
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise credentials_exception


