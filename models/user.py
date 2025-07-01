from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str 

class UserLogin(BaseModel):
    email: str
    password: str

class UserSignUp(BaseModel):
    email: str
    password: str
    username: str 
    phone: str
    profile_pic_url: str

class UserProfile(BaseModel):
    id: str
    email: str
    username: str
    phone: str
    profile_pic_url: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    profile_pic_url: Optional[str]
