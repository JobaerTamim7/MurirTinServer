from pydantic import BaseModel
from datetime import datetime

class ComplaintBase(BaseModel):
    title: str
    description: str
    company_id: int

class ComplaintCreate(ComplaintBase):
    pass

class Complaint(ComplaintBase):
    id: int
    user_id: str
    created_at: datetime
    status: str
