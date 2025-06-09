from models.User import User
from sqlalchemy.orm import Session
from fastapi import HTTPException

def get_user_by_mail(email: str, db_session: Session) -> User:
    try:
        user : User | None = db_session.query(User).filter(User.email == email).first()
        if user == None:
            raise HTTPException(status_code=404,detail="User is not registered.")
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Sever Error.")
    
    return user