from pydantic import EmailStr
from sqlmodel import SQLModel, Field
import uuid


class User(SQLModel, table=True):
    __tablename__ = "user"

    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name : str
    email : EmailStr = Field(unique=True)
    password_hash : str = Field(unique=True)


class Resume(SQLModel, table=True):
    __tablename__ = "resume"

    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    target_job : str
    text: str
    user_id : uuid.UUID = Field(foreign_key="user.id")


class Review(SQLModel, table=True):
    __tablename__ = "review"

    resume_id : uuid.UUID = Field(primary_key=True, foreign_key="resume.id")
    review_score : float = Field(le=10, gt=0)
    strenghts : str
    weaknessess : str
    missing_skills : str
    suggestions : str
