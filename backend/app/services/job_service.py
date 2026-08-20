from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.job_posting import JobPosting
from app.schemas.job_posting import JobPostingCreate
def upsert(db:Session,p:JobPostingCreate)->JobPosting:
    x=db.scalar(select(JobPosting).where(JobPosting.external_job_id==p.external_job_id)); data=p.model_dump()
    if x is None: x=JobPosting(**data); db.add(x)
    else:
        for k,v in data.items(): setattr(x,k,v)
    db.commit(); db.refresh(x); return x
def recent(db:Session,limit:int=50): return list(db.scalars(select(JobPosting).order_by(JobPosting.fetched_at.desc()).limit(limit)).all())
