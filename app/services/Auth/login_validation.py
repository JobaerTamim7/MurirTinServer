from utils.password import verify_pass
from crud.User.get_user_info import get_user_by_mail
from schemas.UserSchema import LoginUserRequest, UserInfo
from models.User import User
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse

def login_validation(req_user: LoginUserRequest, db_session: Session) -> JSONResponse:
    try:
        user: User = get_user_by_mail(req_user.email, db_session)
        is_pass_verified: bool = verify_pass(req_user.password.get_secret_value(),user.hashed_password)

        if is_pass_verified == False:
            raise HTTPException(status_code=401,detail="Wrong password.")
        
        user_info : UserInfo = UserInfo(
                email=user.email,
                user_name=user.user_name,
                mobile_number=user.phone_no,
                payment_methods=[]
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "detail": "Successfully logged in.",
                "user": user_info.model_dump()
            }
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error") 
