#python native
from uuid import UUID
from datetime import date
from typing import Optional

#pydantic
from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

class UserBase(BaseModel):
    user_id: UUID  = Field(
        ...,
        title="User ID",
        description="It is the user id"
    )

    email: EmailStr = Field(
        ...,
        title="Email",
        description="It is the email address of the user",
        example='emailexample@gmail.com'
    )

    user_name: str = Field(
        ...,
        min_length=3,
        max_length=30,
        title="Username",
        description="It is the username",
        example='MyUserName'
    )

class User(UserBase):
    
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        title="First name",
        description="It is the first name of the user",
        example="QueteIm"
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        title="Last name",
        description="It is the last name of the user",
        example="Porta"
    )

    birth_date: Optional[date] = Field(
        title="Date of Birth",
        description="Is the user's date of birth",
        default=None
    )


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        title="Password",
        description="It is the password of the user",
        example="noUseThisPassword00"
    )

class UserRegister(User, UserLogin):
    pass