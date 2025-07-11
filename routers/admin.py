from fastapi import APIRouter, Depends
from services.admin_service import check_user_status
from database import supabase

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/check-user/{email}")
async def api_check_user_status(email: str):

    return await check_user_status(supabase, email)


