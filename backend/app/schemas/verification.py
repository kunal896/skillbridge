from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field
class MicroProjectCreate(BaseModel):
    roadmap_step_id:UUID; skill:str; title:str; description:str; instructions:str; language:str="python"; difficulty:str="beginner"; rubric:list[dict]=[]; test_cases:list[dict]=[]
class MicroProjectRead(MicroProjectCreate):
    id:UUID; created_at:datetime
class SubmissionCreate(BaseModel):
    project_id:UUID; code:str=Field(min_length=1); language:str="python"
class SubmissionRead(SubmissionCreate):
    id:UUID; learner_id:UUID; status:str; submitted_at:datetime
class VerificationResultCreate(BaseModel):
    submission_id:UUID; project_id:UUID; status:str=Field(pattern="^(pass|fail|error)$"); score:float=Field(ge=0,le=100); sandbox_passed:bool; judge_feedback:str|None=None; llm_feedback:str|None=None; unlocks_next:bool=False
class VerificationResultRead(VerificationResultCreate):
    id:UUID; learner_id:UUID; verified_at:datetime
