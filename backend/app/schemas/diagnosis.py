from pydantic import BaseModel
class DiagnosisRequest(BaseModel):
    target_role:str
    resume_text:str|None=None
    mcq_answers:dict[str,str]|None=None
    learner_id:str|None=None
class DiagnosisResponse(BaseModel):
    learner_id:str|None=None
    target_role:str
    current_skills:list[dict]
    skill_gaps:list[dict]
    diagnosis_summary:str
    confidence:float
    roadmap:list[dict]
