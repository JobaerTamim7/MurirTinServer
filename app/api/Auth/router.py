from fastapi import APIRouter, Depends
from schemas.UserSchema import CreateUserRequest
from crud.User.create_user import create_user
from sqlalchemy.orm import Session
from database.database import get_session

auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.post("/register")
async def register(user: CreateUserRequest, db_session: Session = Depends(get_session)):
    return create_user(user,db_session)