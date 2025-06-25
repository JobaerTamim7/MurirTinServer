# models/user.py
from pydantic import BaseModel

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


class UserProfile(BaseModel):
    id: str
    email: str
    username: str
    phone: str

