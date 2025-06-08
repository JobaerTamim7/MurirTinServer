from .Base import Base
from sqlalchemy import String, UniqueConstraint, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4


class User(Base):
    __tablename__ = "user"

    id : Mapped[str] = mapped_column(String, default=lambda : str('u-'+str(uuid4())))
    user_name : Mapped[str] = mapped_column(String)
    email : Mapped[str] = mapped_column(String)
    phone_no : Mapped[str] = mapped_column(String)
    hashed_password : Mapped[str] = mapped_column(String)

    __table_args__ = (
        PrimaryKeyConstraint('id',name='pk_user'),
        UniqueConstraint('email',name='uq_user_email'),
        UniqueConstraint('phone_no',name='uq_user_phone'),
        CheckConstraint('length(phone_no) = 11', name='chk_user_phone_len')
    )
