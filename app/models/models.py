from pydantic import EmailStr
from sqlmodel import Relationship, SQLModel, Field
import uuid
from typing import List


class User(SQLModel, table=True):
    __tablename__ = "user"

    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name : str
    email : EmailStr = Field(unique=True)
    password_hash : str

    resumes : List["Resume"] = Relationship(back_populates="user")


class Resume(SQLModel, table=True):
    __tablename__ = "resume"

    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    target_job : str
    text: str
    user_id : uuid.UUID = Field(foreign_key="user.id")

    user : User = Relationship(back_populates="resumes")

    reviews: List["Review"] = Relationship(back_populates="resume")


class Review(SQLModel, table=True):
    __tablename__ = "review"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    review_score : float = Field(le=10, gt=0)
    strengths : str
    weaknessess : str
    missing_skills : str
    suggestions : str

    resume_id : uuid.UUID = Field(foreign_key="resume.id")
    resume: Resume = Relationship(back_populates="reviews")