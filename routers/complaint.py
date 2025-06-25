# routers/complaint.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.complaint import Complaint, ComplaintCreate
from utils.jwt_token import get_current_user 
from services.complaint_service import create_complaint, get_complaints

router = APIRouter(prefix="/complaints", tags=["complaints"])

@router.post("/", response_model=Complaint, status_code=status.HTTP_201_CREATED)
async def submit_complaint(
    complaint: ComplaintCreate,
    current_user: dict = Depends(get_current_user)
):
    return await create_complaint(complaint, current_user)


@router.get("/", response_model=List[Complaint])
async def list_complaints(
    current_user: dict = Depends(get_current_user) 
):
    return await get_complaints()