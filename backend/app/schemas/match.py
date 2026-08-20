from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
class MatchRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: UUID
    employer_id: UUID
    learner_id: UUID
    role_title: str
    match_score: float = Field(ge=0,le=1)
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    verified_skills: list[str] = Field(default_factory=list)
    explanation: str
    created_at: datetime
