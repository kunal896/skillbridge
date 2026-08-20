from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field
class MatchCreate(BaseModel):
    employer_id:UUID; learner_id:UUID; role_title:str; match_score:float=Field(ge=0,le=1); matched_skills:list[str]=[]; missing_skills:list[str]=[]; verified_skills:list[str]=[]; explanation:str
class MatchRead(MatchCreate):
    id:UUID; created_at:datetime
