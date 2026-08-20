from fastapi import APIRouter,Depends,Query,status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.job_posting import JobPostingCreate,JobPostingRead
from app.services.job_service import upsert,recent
router=APIRouter(prefix="/jobs",tags=["jobs"])
@router.post("",response_model=JobPostingRead,status_code=status.HTTP_201_CREATED)
def create_or_update(p:JobPostingCreate,db:Session=Depends(get_db)):return upsert(db,p)
@router.get("",response_model=list[JobPostingRead])
def list_jobs(limit:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):return recent(db,limit)
