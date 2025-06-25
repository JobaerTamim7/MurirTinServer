from supabase import Client
from fastapi import HTTPException, status
from models.user import UserSignUp, UserProfile

async def sign_up_user(
    supabase: Client,
    user_data: UserSignUp
) -> UserProfile:
    try:
        auth_response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })
        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Auth registration failed"
            )
        
        profile_data = {
            "id": auth_response.user.id,
            "username": user_data.username,
            "email": user_data.email,
            "phone": user_data.phone
        }
        response = supabase.table("user_profiles").insert(profile_data).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            
        return response.data[0]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )