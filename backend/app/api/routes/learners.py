from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_account
from app.db.session import get_db
from app.models.account import Account
from app.schemas.learner import LearnerCreate,LearnerRead
from app.services.learner_service import upsert,by_account,by_id
router=APIRouter(prefix="/learners",tags=["learners"])
@router.put("/me",response_model=LearnerRead)
def me(p:LearnerCreate,a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    if a.role!="learner":raise HTTPException(403,"Learner account required")
    return upsert(db,a.id,p)
@router.get("/me",response_model=LearnerRead)
def get_me(a:Account=Depends(get_current_account),db:Session=Depends(get_db)):
    x=by_account(db,a.id)
    if not x:raise HTTPException(404,"Learner profile not found")
    return x
@router.get("/{learner_id}",response_model=LearnerRead)
def get_public(learner_id:UUID,db:Session=Depends(get_db)):
    x=by_id(db,learner_id)
    if not x:raise HTTPException(404,"Learner not found")
    return x
