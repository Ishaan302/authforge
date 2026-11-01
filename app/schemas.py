# we check whether the incomming data is valid or not before saving anything to postgresql 

from pydantic import BaseModel, EmailStr, Field


class UserRegistered(BaseModel):  # for new user 
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):   # for existing user 
    email: EmailStr
    password: str