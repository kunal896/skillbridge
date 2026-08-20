from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field
class MicroProjectCreate(BaseModel):
    roadmap_step_id: UUID
    skill: str
    title: str
    description: str
    instructions: str
    language: str = "python"
    difficulty: str = "beginner"
    rubric: list[dict] = Field(default_factory=list)
    test_cases: list[dict] = Field(default_factory=list)
class MicroProjectRead(MicroProjectCreate):
    id: UUID
    created_at: datetime
class SubmissionCreate(BaseModel):
    node_id: UUID
    code: str = Field(min_length=1)
    language: str = "python"
    project_id: UUID | None = None
class SubmissionRead(BaseModel):
    id: UUID
    learner_id: UUID
    project_id: UUID
    code: str
    language: str
    status: str
    submitted_at: datetime
class VerificationResultRead(BaseModel):
    id: UUID
    submission_id: UUID
    project_id: UUID
    learner_id: UUID
    status: str
    score: float
    sandbox_passed: bool
    judge_feedback: str | None
    llm_feedback: str | None
    unlocks_next: bool
    verified_at: datetime
