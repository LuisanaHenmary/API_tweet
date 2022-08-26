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
    user_id: UUID  = Field(...)

    email: EmailStr = Field(
        ...,
        example='sebas@sebas.com'
    )

    user_name: str = Field(
        ...,
        min_length=3,
        max_length=10,
        example='sgewux'
    )

class User(UserBase):
    
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=30
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=30
    )

    birth_date: Optional[date] = Field(
        default=None
    )


class UserLogin(UserBase):
    password: str = Field(
        ...,
        example="noUseThis00",
        min_length=8,
        max_length=64
    )

class UserRegister(User, UserLogin):
    pass