from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime
from database import supabase
from models.complaint import ComplaintCreate, Complaint
from models.company import Company

async def get_all_companies(current_user: dict) -> List[Company]:
    """
    Fetches all bus companies from the 'bus_company' table.
    Requires a valid authenticated user.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to view companies."
        )
    
    try:
        response = supabase.table('bus_company').select("id, name").execute()
        if response.data:
            companies = [Company(id=item['id'], name=item['name']) for item in response.data]
            return companies
        return []
    except Exception as e:
        print(f"Error fetching companies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch companies."
        )

async def create_complaint(complaint: ComplaintCreate, current_user: dict) -> Optional[dict]:
    """
    Inserts a new complaint into the 'complaint' table.
    Requires a valid authenticated user.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to submit a complaint."
        )
    
    try:
        complaint_dict = complaint.model_dump()
        complaint_dict['user_id'] = user_id
        complaint_dict['created_at'] = datetime.now().isoformat()
        complaint_dict['status'] = 'submitted' 
        complaint_dict['ticket_id'] = complaint.ticket_id 

        response = supabase.table('complaints').insert(complaint_dict).execute()

        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to insert complaint into database."
            )
    except Exception as e:
        print(f"Error creating complaint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while submitting the complaint."
        )
async def get_all_complaints(current_user: dict) -> List[Complaint]:
    """
    Fetches all user complaints from the 'complaints' table.
    Requires a valid authenticated user.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to view complaints."
        )

    try:
        response = supabase.table('complaints').select("*").order('created_at', desc=True).execute()
        if response.data:
            complaints = [Complaint(**item) for item in response.data]
            return complaints
        return []
    except Exception as e:
        print(f"Error fetching complaints: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch complaints."
        )


async def get_user_complaints(current_user: dict) -> List[Complaint]:
    """
    Fetch complaints submitted by the currently authenticated user.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )

    try:
        response = supabase.table('complaints') \
            .select("*") \
            .eq("user_id", user_id) \
            .order('created_at', desc=True) \
            .execute()

        if response.data:
            return [Complaint(**item) for item in response.data]
        return []

    except Exception as e:
        print(f"Error fetching user's complaints: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch complaints for this user."
        )
    

async def get_complaint_by_id(complaint_id: int, current_user: dict) -> Complaint:
    """
    Retrieve a specific complaint by ID, only if it belongs to the current user.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )

    try:
        response = supabase.table("complaints") \
            .select("*") \
            .eq("id", complaint_id) \
            .eq("user_id", user_id) \
            .single() \
            .execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found or access denied."
            )

        return Complaint(**response.data)

    except Exception as e:
        print(f"Error fetching complaint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve complaint details."
        )