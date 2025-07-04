from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.complaint import Complaint
from utils.jwt_token import get_current_user 
from services.complaint_service import get_all_complaints,get_complaint_by_id

router = APIRouter(prefix="/issues")

@router.get("/",response_model=List[Complaint], status_code=status.HTTP_200_OK)
async def social_issues_api(current_user: dict = Depends(get_current_user)):
    return await get_all_complaints(current_user)




