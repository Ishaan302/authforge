# we check whether the incomming data is valid or not before saving anything to postgresql 

from pydantic import BaseModel, EmailStr, Field


class UserRegistered(BaseModel):
    email: EmailStr
    password: str = Field(min_length=9, max_length=128)