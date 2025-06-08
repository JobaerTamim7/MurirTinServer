from pydantic import BaseModel, SecretStr, ConfigDict, EmailStr, Field
from typing import List

class UserSchema(BaseModel):
    email : EmailStr

    model_config = ConfigDict(from_attributes=True)

class LoginUserRequest(UserSchema):
    password : SecretStr

class CreateUserRequest(UserSchema):
    user_name : str
    password : SecretStr
    phone_number : str = Field(max_length=11, min_length=11)

class UserInfo(UserSchema):
    user_name : str
    mobile_number : str = Field(max_length=11, min_length=11)
    email : EmailStr
    payment_methods : List[str]