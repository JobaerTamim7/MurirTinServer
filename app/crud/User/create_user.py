from schemas.UserSchema import CreateUserRequest
from sqlalchemy.orm import Session
from models.User import User
from utils.password import password_hashing
from sqlalchemy.exc import IntegrityError

def create_user(user: CreateUserRequest, db_session: Session):
    new_user = User(
        user_name = user.user_name,
        email = user.email,
        phone_no = user.phone_number,
        hashed_password = password_hashing(user.password.get_secret_value())
    )
    try:
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
    except IntegrityError:
        db_session.rollback()
        raise 
    except Exception as e:
        db_session.rollback()
        raise Exception(f"An error occurred while creating the user: {str(e)}")

