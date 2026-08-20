from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,Field
class RoadmapStepCreate(BaseModel):
    skill:str; title:str; description:str; reason:str; step_order:int=Field(ge=1); citations:list[dict]=[]
class RoadmapCreate(BaseModel):
    target_role:str; overall_summary:str|None=None; steps:list[RoadmapStepCreate]
class RoadmapStepRead(RoadmapStepCreate):
    id:UUID; roadmap_id:UUID; status:str
class RoadmapRead(BaseModel):
    id:UUID; learner_id:UUID; target_role:str; overall_summary:str|None; status:str; created_at:datetime; steps:list[RoadmapStepRead]
