from models.User import User
from sqlalchemy.orm import Session
from exceptions import UserNotFoundError

def get_user_by_mail(email: str, db_session: Session) -> User:
    user : User | None = db_session.query(User).filter(User.email == email).first()
    if user == None:
        raise UserNotFoundError("User not found")   
    return user