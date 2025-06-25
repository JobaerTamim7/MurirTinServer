from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ComplaintBase(BaseModel):
    title: str
    description: str

class ComplaintCreate(ComplaintBase):
    pass

class Complaint(ComplaintBase):
    id: int
    user_id: str
    created_at: Optional[datetime] 
