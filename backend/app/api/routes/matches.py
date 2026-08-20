from uuid import UUID
from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_account
from app.db.session import get_db
from app.schemas.match import MatchCreate,MatchRead
from app.services.match_service import save,learner_matches
router=APIRouter(prefix="/matches",tags=["matches"])
@router.post("",response_model=MatchRead)
def create_match(p:MatchCreate,db:Session=Depends(get_db)):return save(db,p)
@router.get("/learner/{learner_id}",response_model=list[MatchRead])
def get_matches(learner_id:UUID,limit:int=Query(50,ge=1,le=100),db:Session=Depends(get_db),_=Depends(get_current_account)):return learner_matches(db,learner_id,limit)
