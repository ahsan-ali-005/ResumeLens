from datetime import datetime, timezone
from pydantic import EmailStr
from sqlmodel import DateTime, Relationship, SQLModel, Field
import uuid
from typing import List


class User(SQLModel, table=True):
    __tablename__ = "user"

    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name : str
    email : EmailStr = Field(unique=True)
    password_hash : str
    is_verified : bool = Field(default=False)
    resumes : List["Resume"] = Relationship(back_populates="user")


class Resume(SQLModel, table=True):
    __tablename__ = "resume"

    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    target_job : str
    text: str
    user_id : uuid.UUID = Field(foreign_key="user.id")
    filename : str
    created_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True))
    user : User = Relationship(back_populates="resumes")
    reviews: List["Review"] = Relationship(back_populates="resume")


class Review(SQLModel, table=True):
    __tablename__ = "review"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    review_score : float = Field(le=10, gt=0)
    strengths : str
    weaknesses : str
    missing_skills : str
    suggestions : str
    resume_id : uuid.UUID = Field(foreign_key="resume.id")
    resume: Resume = Relationship(back_populates="reviews")