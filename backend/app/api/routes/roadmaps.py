import json
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_account
from app.db.session import get_db
from app.models.account import Account
from app.models.learner import Learner
from app.models.roadmap import RoadmapStep
from app.schemas.roadmap import RoadmapCreate,RoadmapRead,RoadmapStepRead
from app.services.roadmap_service import create,create_from_agent_roadmap,get
from app.services.diagnosis_service import run_diagnosis_pipeline
router=APIRouter(prefix="/roadmaps",tags=["roadmaps"])
def serialize(pair):
    r,steps=pair
    return RoadmapRead(id=r.id,learner_id=r.learner_id,target_role=r.target_role,overall_summary=r.overall_summary,status=r.status,created_at=r.created_at,steps=[RoadmapStepRead(id=s.id,roadmap_id=s.roadmap_id,skill=s.skill,title=s.title,description=s.description,reason=s.reason,step_order=s.step_order,status=s.status,citations=json.loads(s.citations_json)) for s in steps])
@router.post("",response_model=RoadmapRead)
def create_route(learner_id:UUID,p:RoadmapCreate,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    x=db.get(Learner,learner_id)
    if a.role!="learner" or not x or x.account_id!=a.id:raise HTTPException(403,"Cannot create roadmap for this learner")
    r=create(db,learner_id,p)
    return serialize((r,list(db.scalars(select(RoadmapStep).where(RoadmapStep.roadmap_id==r.id).order_by(RoadmapStep.step_order)).all())))
@router.post("/generate",response_model=RoadmapRead)
def generate_route(learner_id:UUID,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    """Runs the diagnose -> plan agent pipeline against the learner's stored
    profile and persists the resulting cited roadmap. Replaces the old
    pattern of the client submitting pre-built steps for /roadmaps (create
    route above) with the pipeline itself deciding sequencing and citations."""
    x=db.get(Learner,learner_id)
    if a.role!="learner" or not x or x.account_id!=a.id:raise HTTPException(403,"Cannot generate roadmap for this learner")
    if not x.resume_text:raise HTTPException(400,"Learner has no resume_text on file; complete onboarding diagnosis first")
    final_state=run_diagnosis_pipeline(target_role=x.target_role,resume_text=x.resume_text,learner_id=str(learner_id))
    agent_roadmap=final_state.get("roadmap",[])
    if final_state.get("status")=="failed" or not agent_roadmap:raise HTTPException(502,"Roadmap generation failed. Please try again.")
    r=create_from_agent_roadmap(db,learner_id,x.target_role,final_state.get("diagnosis_summary"),agent_roadmap)
    return serialize((r,list(db.scalars(select(RoadmapStep).where(RoadmapStep.roadmap_id==r.id).order_by(RoadmapStep.step_order)).all())))
@router.get("/{roadmap_id}",response_model=RoadmapRead)
def read_route(roadmap_id:UUID,db:Session=Depends(get_db)):
    pair=get(db,roadmap_id)
    if pair[0] is None:raise HTTPException(404,"Roadmap not found")
    return serialize(pair)
