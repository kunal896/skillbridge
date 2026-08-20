import json
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_account
from app.db.session import get_db
from app.models.account import Account
from app.models.employer import Employer, EmployerRequirement
from app.models.learner import Learner
from app.schemas.match import MatchRead
from app.services.match_service import compute_and_save, learner_matches
router=APIRouter(prefix="/matches",tags=["matches"])

@router.get("/employer/{employer_id}",response_model=list[MatchRead])
def rank_for_employer(
    employer_id: UUID,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Account = Depends(get_current_account),
):
    employer=db.get(Employer,employer_id)
    if not employer: raise HTTPException(404,"Employer not found")
    reqs=list(db.scalars(select(EmployerRequirement).where(EmployerRequirement.employer_id==employer_id)).all())
    if not reqs: return []
    learners=list(db.scalars(select(Learner)).all())
    return compute_and_save(db, employer_id, reqs[0], learners, limit)

@router.get("/learner/{learner_id}",response_model=list[MatchRead])
def get_matches(learner_id:UUID,limit:int=Query(50,ge=1,le=100),db:Session=Depends(get_db),_=Depends(get_current_account)):
    return learner_matches(db,learner_id,limit)
