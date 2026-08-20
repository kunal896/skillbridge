from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_account
from app.db.session import get_db
from app.models.account import Account
from app.models.learner import Learner
from app.models.roadmap import RoadmapStep
from app.schemas.verification import MicroProjectCreate,MicroProjectRead,SubmissionCreate,SubmissionRead,VerificationResultRead
from app.services.verification_service import project,submit_and_verify,history
router=APIRouter(prefix="/verification",tags=["verification"])

def learner_for(a,db):
    if a.role!="learner": raise HTTPException(403,"Learner account required")
    x=db.scalar(select(Learner).where(Learner.account_id==a.id))
    if not x: raise HTTPException(404,"Learner profile not found")
    return x

@router.post("/projects",response_model=MicroProjectRead)
def create_project(p:MicroProjectCreate,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    learner_for(a,db); return project(db,p)

@router.post("/submissions",response_model=VerificationResultRead)
def submit_code(p:SubmissionCreate,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    learner=learner_for(a,db)
    try:
        return submit_and_verify(db,learner,p)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history",response_model=list[VerificationResultRead])
def get_history(a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    return history(db,learner_for(a,db).id)
