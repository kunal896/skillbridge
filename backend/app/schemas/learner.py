from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,ConfigDict,Field
from shared.types.types import ProfileSource
class LearnerCreate(BaseModel):
    current_role: str|None=Field(default=None,max_length=120)
    target_role: str=Field(min_length=1,max_length=120)
    preferred_region: str|None=Field(default=None,max_length=120)
    preferred_language: str|None=Field(default=None,max_length=80)
    resume_text: str|None=None
    profile_source: ProfileSource=ProfileSource.MANUAL
class LearnerRead(LearnerCreate):
    model_config=ConfigDict(from_attributes=True)
    id: UUID
    account_id: UUID
    created_at: datetime
    updated_at: datetime
