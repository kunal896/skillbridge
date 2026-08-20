from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,ConfigDict,Field
class JobPostingCreate(BaseModel):
    external_job_id:str=Field(min_length=1,max_length=160)
    title:str=Field(min_length=1,max_length=200)
    company:str|None=None; location:str|None=None; region:str|None=None
    description:str=Field(min_length=1)
    source_name:str=Field(min_length=1,max_length=80)
    source_url:str=Field(min_length=1,max_length=1000)
    posted_at:datetime|None=None
    freshness_score:float|None=Field(default=None,ge=0,le=1)
class JobPostingRead(JobPostingCreate):
    model_config=ConfigDict(from_attributes=True)
    id:UUID; fetched_at:datetime
