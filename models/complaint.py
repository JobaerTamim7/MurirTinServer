from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
class ComplaintBase(BaseModel):
    title: str
    description: str
    company_id: int
    ticket_id: Optional[str] = None

class ComplaintCreate(ComplaintBase):
    pass

class Complaint(ComplaintBase):
    id: int
    user_id: str
    created_at: datetime
    status: str

class ComplaintWithTicket(Complaint):
    ticket_from_location: Optional[str] = None
    ticket_to_location: Optional[str] = None

