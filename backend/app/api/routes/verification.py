from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_account
from app.db.session import get_db
from app.models.account import Account
from app.models.learner import Learner
from app.schemas.verification import MicroProjectCreate,MicroProjectRead,SubmissionCreate,SubmissionRead,VerificationResultCreate,VerificationResultRead
from app.services.verification_service import project,submit,result,history
router=APIRouter(prefix="/verification",tags=["verification"])
def learner_for(a,db):
    if a.role!="learner":raise HTTPException(403,"Learner account required")
    x=db.query(Learner).filter(Learner.account_id==a.id).first()
    if not x:raise HTTPException(404,"Learner profile not found")
    return x
@router.post("/projects",response_model=MicroProjectRead)
def create_project(p:MicroProjectCreate,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):learner_for(a,db);return project(db,p)
@router.post("/submissions",response_model=SubmissionRead)
def submit_code(p:SubmissionCreate,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    return submit(db,learner_for(a,db).id,p)
@router.post("/results",response_model=VerificationResultRead)
def record(p:VerificationResultCreate,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    return result(db,learner_for(a,db).id,p)
@router.get("/history",response_model=list[VerificationResultRead])
def get_history(a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    return history(db,learner_for(a,db).id)
