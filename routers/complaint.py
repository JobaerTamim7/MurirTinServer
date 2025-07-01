# routers/complaint.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.complaint import Complaint, ComplaintCreate
from utils.jwt_token import get_current_user 
from services.complaint_service import get_all_companies, create_complaint

router = APIRouter(prefix="/complaints", tags=["complaints"])

@router.get("/companies")
async def get_companies(current_user: dict = Depends(get_current_user)):
    return await get_all_companies(current_user)

@router.post("/", response_model=Complaint, status_code=status.HTTP_201_CREATED)
async def create_complaint_api(complaint: ComplaintCreate, current_user: dict = Depends(get_current_user)):
    return await create_complaint(complaint, current_user)