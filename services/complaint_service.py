from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime
from database import supabase
from models.complaint import ComplaintCreate
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
        complaint_dict['status'] = 'pending'  

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
