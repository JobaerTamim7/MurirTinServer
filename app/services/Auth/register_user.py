from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from schemas.UserSchema import CreateUserRequest
from crud.User.create_user import create_user

def register_user(user: CreateUserRequest, db_session: Session) -> JSONResponse | None:
    try:
        create_user(user, db_session)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"detail": "User registered successfully."}
        )
    except Exception as error:
        handleError(error)
    
def handleError(error: Exception):
    if isinstance(error, IntegrityError):
        raise HTTPException(status_code=400, detail="Email or phone number already exists.")
    else:
        raise HTTPException(status_code=500, detail=f"Internal Server Error. {str(error)}")