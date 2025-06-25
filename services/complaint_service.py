from fastapi import HTTPException, status
from supabase import Client
from database import supabase
from models.complaint import Complaint, ComplaintCreate
from utils.jwt_token import get_current_user
from typing import List
from fastapi import Depends

async def create_complaint(
    complaint: ComplaintCreate,
    current_user: dict = Depends(get_current_user)
):
    try:
        response = supabase.table("complaints").insert({
            "user_id": current_user["sub"], 
            "title": complaint.title,
            "description": complaint.description
        }).execute()
        
        complaint_data = response.data[0]
        return {
            "id": int(complaint_data["id"]),
            "user_id": str(complaint_data["user_id"]),
            "title": complaint_data["title"],
            "description": complaint_data["description"],
            "created_at": complaint_data["created_at"],
            "username": "current_user"  
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_complaints():
    try:
        response = supabase.table("complaints").select("""
            id,
            title,
            description,
            created_at,
            user_id,
            user_profiles:user_id(username)
        """).order("created_at", desc=True).execute()

        return [{
            "id": int(complaint["id"]), 
            "title": complaint["title"],
            "description": complaint["description"],
            "created_at": complaint["created_at"],
            "user_id": str(complaint["user_id"]), 
            "username": complaint["user_profiles"]["username"]
        } for complaint in response.data]
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))