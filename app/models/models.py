import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, List, Optional

from pydantic import EmailStr
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel, DateTime


def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class ReviewStatus(str, Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: EmailStr = Field(unique=True)
    password_hash: str
    is_verified: bool = Field(default=False)

    resumes: List["Resume"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "passive_deletes": True},
    )


class Resume(SQLModel, table=True):
    __tablename__ = "resume"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE", index=True)
    filename: str
    text: str
    parsed_data: Optional[dict[str, Any]] = Field(
        default=None, sa_column=Column(JSONB(none_as_null=True), nullable=True)
    )
    created_at: datetime = Field(default_factory=utcnow, sa_type=DateTime(timezone=True))

    user: User = Relationship(back_populates="resumes")
    reviews: List["Review"] = Relationship(
        back_populates="resume",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "passive_deletes": True},
    )


class Review(SQLModel, table=True):
    __tablename__ = "review"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    resume_id: uuid.UUID = Field(foreign_key="resume.id", ondelete="CASCADE", index=True)
    target_job: str
    job_description: str
    status: str = Field(default=ReviewStatus.PENDING.value)
    overall_score: Optional[float] = Field(default=None)
    details: Optional[dict[str, Any]] = Field(
        default=None, sa_column=Column(JSONB(none_as_null=True), nullable=True)
    )
    model_name: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utcnow, sa_type=DateTime(timezone=True))

    resume: Resume = Relationship(back_populates="reviews")