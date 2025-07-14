# routers/complaint.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.complaint import Complaint, ComplaintCreate
from utils.jwt_token import get_current_user 
from services.complaint_service import get_all_companies,create_complaint,get_user_complaints, get_complaint_by_id 
from services.react_service import toggle_like, get_complaint_likes, get_complaints_with_likes
from models.react import ReactResponse, ComplaintWithReactions


router = APIRouter(prefix="/complaints", tags=["complaints"])

@router.get("/companies")
async def get_companies(current_user: dict = Depends(get_current_user)):
    return await get_all_companies(current_user)

@router.post("/", response_model=Complaint, status_code=status.HTTP_201_CREATED)
async def create_complaint_api(complaint: ComplaintCreate, current_user: dict = Depends(get_current_user)):
    return await create_complaint(complaint, current_user)

@router.get("/user", response_model=List[Complaint])
async def user_complaints_api(current_user: dict = Depends(get_current_user)):
    return await get_user_complaints(current_user)

@router.get("/{complaint_id}", response_model=Complaint)
async def get_complaint_details_api(
    complaint_id: int,
    current_user: dict = Depends(get_current_user)
):
    return await get_complaint_by_id(complaint_id, current_user)

@router.post("/{complaint_id}/like", response_model=ReactResponse)
async def like_complaint(
    complaint_id: int,
    current_user: dict = Depends(get_current_user)
):
    return await toggle_like(complaint_id, True, current_user)

@router.post("/{complaint_id}/dislike", response_model=ReactResponse)
async def dislike_complaint(
    complaint_id: int,
    current_user: dict = Depends(get_current_user)
):
    return await toggle_like(complaint_id, False, current_user)

@router.get("/{complaint_id}/likes", response_model=ReactResponse)
async def get_complaint_likes_api(
    complaint_id: int,
    current_user: dict = Depends(get_current_user)
):
    return await get_complaint_likes(complaint_id, current_user)

@router.get("/social/all", response_model=List[ComplaintWithReactions])
async def get_all_complaints_with_likes(
    current_user: dict = Depends(get_current_user)
):
    return await get_complaints_with_likes(current_user)
