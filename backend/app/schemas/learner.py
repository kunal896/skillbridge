from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from shared.types.types import ProfileSource

class SkillInput(BaseModel):
    name: str
    level: str = "beginner"
    evidence: list[str] = Field(default_factory=list)

class LearnerCreate(BaseModel):
    current_role: str | None = Field(default=None, max_length=120)
    target_role: str = Field(min_length=1, max_length=120)
    preferred_region: str | None = Field(default=None, max_length=120)
    preferred_language: str | None = Field(default=None, max_length=80)
    resume_text: str | None = None
    skills: list[SkillInput] = Field(default_factory=list)
    verified_skills: list[str] = Field(default_factory=list)
    experience_years: int | None = Field(default=None, ge=0)
    education: str | None = None
    profile_source: ProfileSource = ProfileSource.MANUAL

class LearnerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    account_id: UUID
    current_role: str | None
    target_role: str
    preferred_region: str | None
    preferred_language: str | None
    resume_text: str | None
    skills: list[SkillInput]
    verified_skills: list[str]
    experience_years: int | None
    education: str | None
    profile_source: ProfileSource
    created_at: datetime
    updated_at: datetime
