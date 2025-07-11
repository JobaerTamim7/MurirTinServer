from supabase import Client
from fastapi import HTTPException, status

async def check_user_status(supabase: Client, email: str):

    try:
        profile_response = supabase.table("user_profiles").select("*").eq("email", email).execute()
        profile_exists = bool(profile_response.data)
        
        return {
            "email": email,
            "profile_exists": profile_exists,
            "message": f"Profile exists: {profile_exists}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking user status: {str(e)}"
        )


