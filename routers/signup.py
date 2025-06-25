from fastapi import APIRouter, Depends
from services.signup_service import sign_up_user
from models.user import UserSignUp, UserProfile
from database import supabase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserProfile)
async def api_sign_up_user(
    user_data: UserSignUp
):
    return await sign_up_user(supabase, user_data)