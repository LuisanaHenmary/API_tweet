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

    """
        This class, which descends from BaseModel,
        It's the base for any model related to the usar
    """

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

    """
        This class, which descends from UserBase,
        It's to display all user information, except password
    """
    
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


class UserAuth(UserBase):

    """
        This class, which descends from UserBase,
        It's to enter the password
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        title="Password",
        description="It is the password of the user",
        example="noUseThisPassword00"
    )

class UserRegister(User, UserAuth):
    """
        This class, which descends from User and UserAuth,
        It is to enter the user data, when registering
    """
    pass