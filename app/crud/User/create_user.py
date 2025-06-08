from schemas.UserSchema import CreateUserRequest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.User import User
from fastapi import HTTPException
from fastapi.responses import JSONResponse

def create_user(user: CreateUserRequest, db_session: Session):
    try:
        new_user = User(
            user_name = user.user_name,
            email = user.email,
            phone_no = user.phone_number,
            hashed_password = user.password.get_secret_value()
        )

        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        return JSONResponse(status_code=201,content={"detail": "Successfully added user.", "id":new_user.id})

    except IntegrityError:
        db_session.rollback()
        raise HTTPException(status_code=400, detail="User with this email or phone number already exist.")
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error. {str(e)}")