from fastapi import APIRouter, Depends
from schemas.UserSchema import CreateUserRequest,LoginUserRequest
from services.Auth.login_validation import login_validation
from services.Auth.register_user import register_user
from sqlalchemy.orm import Session
from models.User import User
from database.database import get_session

auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.post("/register")
async def register(user: CreateUserRequest, db_session: Session = Depends(get_session)):
    return register_user(user,db_session)

@auth_router.post("/login")
async def login(req_user: LoginUserRequest, db_session: Session = Depends(get_session)):
    return login_validation(req_user,db_session)
