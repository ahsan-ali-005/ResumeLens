from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    name : str
    email : EmailStr
    password : str = Field(min_length=8)
