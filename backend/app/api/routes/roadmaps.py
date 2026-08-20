import json
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_account
from app.db.session import get_db
from app.models.account import Account
from app.models.learner import Learner
from app.models.roadmap import Roadmap,RoadmapStep
from app.schemas.roadmap import RoadmapRead,RoadmapStepRead
from app.services.roadmap_service import create_from_agent_roadmap,get
from app.services.diagnosis_service import run_diagnosis_pipeline
router=APIRouter(prefix="/roadmaps",tags=["roadmaps"])

def serialize(pair):
    r,steps=pair
    return RoadmapRead(id=r.id,learner_id=r.learner_id,target_role=r.target_role,overall_summary=r.overall_summary,status=r.status,created_at=r.created_at,steps=[RoadmapStepRead(id=s.id,roadmap_id=s.roadmap_id,skill=s.skill,title=s.title,description=s.description,reason=s.reason,step_order=s.step_order,status=s.status,citations=json.loads(s.citations_json)) for s in steps])

@router.get("/learner/{learner_id}",response_model=RoadmapRead)
def learner_roadmap(learner_id:UUID,db:Session=Depends(get_db)):
    r=db.scalar(select(Roadmap).where(Roadmap.learner_id==learner_id).order_by(Roadmap.created_at.desc()))
    if not r: raise HTTPException(404,"Roadmap not found")
    return serialize(get(db,r.id))

@router.post("/generate",response_model=RoadmapRead)
def generate_route(learner_id:UUID,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    x=db.get(Learner,learner_id)
    if a.role!="learner" or not x or x.account_id!=a.id: raise HTTPException(403,"Cannot generate roadmap for this learner")
    if not x.resume_text and not x.current_role: raise HTTPException(400,"Complete learner onboarding first")
    final_state=run_diagnosis_pipeline(target_role=x.target_role,resume_text=x.resume_text,mcq_answers=None,learner_id=str(learner_id))
    if final_state.get("status")=="failed" or not final_state.get("roadmap"): raise HTTPException(502,"Roadmap generation failed")
    r=create_from_agent_roadmap(db,learner_id,x.target_role,final_state.get("diagnosis_summary"),final_state["roadmap"])
    return serialize(get(db,r.id))

@router.get("/{roadmap_id}",response_model=RoadmapRead)
def read_route(roadmap_id:UUID,db:Session=Depends(get_db)):
    pair=get(db,roadmap_id)
    if pair[0] is None: raise HTTPException(404,"Roadmap not found")
    return serialize(pair)
