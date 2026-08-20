from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.learner import Learner
from app.schemas.learner import LearnerCreate
def upsert(db:Session,account_id:UUID,payload:LearnerCreate)->Learner:
    x=db.scalar(select(Learner).where(Learner.account_id==account_id)); data=payload.model_dump()
    if x is None: x=Learner(account_id=account_id,**data); db.add(x)
    else:
        for k,v in data.items(): setattr(x,k,v)
    db.commit(); db.refresh(x); return x
def by_account(db:Session,account_id:UUID): return db.scalar(select(Learner).where(Learner.account_id==account_id))
def by_id(db:Session,learner_id:UUID): return db.scalar(select(Learner).where(Learner.id==learner_id))
