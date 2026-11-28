from typing import List, Literal, Optional
from uuid import UUID
from pydantic import ConfigDict
from pydantic import BaseModel, EmailStr, Field, model_validator

class CreateUser(BaseModel):
    name : str
    email : EmailStr
    password : str = Field(min_length=8)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)
    confirm_password : str

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    email: EmailStr
    is_verified: bool


class KeywordMatch(BaseModel):
    """Which important keywords from the job description the resume has and lacks."""

    matched: List[str] = Field(description="Important keywords from the job description that ARE present in the resume.")
    missing: List[str] = Field(description="Important keywords from the job description that are NOT present in the resume.")


class SectionFeedback(BaseModel):
    """Review of one resume section."""

    section: Literal["contact", "summary", "skills", "experience", "education", "projects"] = Field(description="Which resume section this feedback is about.")
    score: int = Field(ge=0, le=10, description="Whole-number quality score of this section, 0 to 10.")
    comment: str = Field(description="1 to 2 sentences explaining the score. Mention only what is in the resume.")


class Suggestion(BaseModel):
    """One specific, actionable improvement."""

    section: Literal["contact", "summary", "skills", "experience", "education", "projects", "general"] = Field(description="Section this suggestion applies to; use 'general' for resume-wide issues like length or formatting.")
    issue: str = Field(description="The single problem found, stated specifically.")
    fix: str = Field(description="A concrete fix for that exact problem.")
    priority: Literal["low", "medium", "high"] = Field(description="How important it is to fix this.")


class ReviewResult(BaseModel):
    """Structured review of a resume against a target job and its job description."""

    summary: str = Field(description="2 to 4 sentence overall assessment of the resume for this job.")
    strengths: List[str] = Field(description="3 to 6 strong points, each specific to this resume.")
    weaknesses: List[str] = Field(description="3 to 6 weak points, each specific to this resume.")
    missing_skills: List[str] = Field(description="Skills or technologies the job requires that the resume does not show.")
    keyword_match: KeywordMatch
    section_feedback: List[SectionFeedback] = Field(description="Exactly one entry for each of the six sections: contact, summary, skills, experience, education, projects.")
    suggestions: List[Suggestion] = Field(description="Prioritised, actionable improvements. One issue and one fix per item.")

class Contact(BaseModel):
    """Contact details exactly as written on the resume. Never invent anything; use null when absent."""

    name: Optional[str] = Field(default=None, description="Full name as written on the resume.")
    email: Optional[str] = Field(default=None, description="Email address as written.")
    phone: Optional[str] = Field(default=None, description="Phone number as written.")
    location: Optional[str] = Field(default=None, description="City/country or address as written.")
    links: List[str] = Field(
        default_factory=list,
        description="Every URL or profile link on the resume (GitHub, LinkedIn, portfolio, etc.), as written.",
    )


class Experience(BaseModel):
    """One job, internship or work experience entry, exactly as written. Never invent details."""

    role: Optional[str] = Field(default=None, description="Job title or role.")
    company: Optional[str] = Field(default=None, description="Company or organisation name.")
    start: Optional[str] = Field(default=None, description="Start date as written, e.g. 'Jan 2024'.")
    end: Optional[str] = Field(default=None, description="End date as written, e.g. 'Mar 2025' or 'Present'.")
    bullets: List[str] = Field(
        default_factory=list,
        description="Each responsibility/achievement bullet point of this entry, one string per bullet, as written.",
    )


class Education(BaseModel):
    """One education entry, exactly as written. Never invent details."""

    institute: Optional[str] = Field(default=None, description="School/college/university name.")
    degree: Optional[str] = Field(default=None, description="Degree, program or certificate title.")
    start: Optional[str] = Field(default=None, description="Start date as written.")
    end: Optional[str] = Field(default=None, description="End date as written, or expected graduation.")


class Project(BaseModel):
    """One personal/academic/professional project entry, exactly as written. Never invent details."""

    name: Optional[str] = Field(default=None, description="Project name.")
    tech: List[str] = Field(
        default_factory=list,
        description="Tools, technologies and stack mentioned for this project, one string each.",
    )
    bullets: List[str] = Field(
        default_factory=list,
        description="Each description/achievement bullet of this project, one string per bullet, as written.",
    )


class ParsedResume(BaseModel):
    """Resume text converted into structured sections. Extract ONLY what is written in the resume: do not
    invent, infer or improve anything; use null or an empty list for anything not present."""

    contact: Optional[Contact] = Field(default=None, description="Contact details section.")
    summary: Optional[str] = Field(default=None, description="About/profile/objective text, as written.")
    skills: List[str] = Field(
        default_factory=list,
        description="All skills, tools, technologies, languages and soft skills listed, one string each.",
    )
    experience: List[Experience] = Field(default_factory=list, description="Work experience entries.")
    education: List[Education] = Field(default_factory=list, description="Education entries.")
    projects: List[Project] = Field(default_factory=list, description="Project entries.")
    other: List[str] = Field(
        default_factory=list,
        description="Anything that fits none of the sections above (certifications, achievements, awards, etc.), one string each.",
    )