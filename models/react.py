from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ReactBase(BaseModel):
    complaint_id: int
    is_liked: bool

class ReactCreate(ReactBase):
    pass

class React(ReactBase):
    id: int
    user_id: str
    created_at: datetime

class ReactResponse(BaseModel):
    message: str
    like_count: int
    dislike_count: int
    user_reaction: Optional[bool] = None

class ComplaintWithReactions(BaseModel):
    id: int
    title: str
    description: str
    company_id: int
    user_id: str
    ticket_id: Optional[str] = None
    created_at: datetime
    status: str
    like_count: int
    dislike_count: int
    user_reaction: Optional[bool] = None
    
    