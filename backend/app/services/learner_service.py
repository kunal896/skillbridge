import json
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.learner import Learner
from app.schemas.learner import LearnerCreate, SkillInput

def _to_db(payload: LearnerCreate) -> dict:
    data = payload.model_dump()
    data["skills_json"] = json.dumps(data.pop("skills", []))
    data["verified_skills_json"] = json.dumps(data.pop("verified_skills", []))
    return data

def _attach_contract(obj: Learner) -> Learner:
    obj.skills = json.loads(obj.skills_json or "[]")
    obj.verified_skills = json.loads(obj.verified_skills_json or "[]")
    return obj

def upsert(db: Session, account_id: UUID, payload: LearnerCreate) -> Learner:
    x = db.scalar(select(Learner).where(Learner.account_id == account_id))
    data = _to_db(payload)
    if x is None:
        x = Learner(account_id=account_id, **data)
        db.add(x)
    else:
        for k, v in data.items():
            setattr(x, k, v)
    db.commit(); db.refresh(x)
    return _attach_contract(x)

def by_account(db: Session, account_id: UUID):
    x = db.scalar(select(Learner).where(Learner.account_id == account_id))
    return _attach_contract(x) if x else None

def by_id(db: Session, learner_id: UUID):
    x = db.scalar(select(Learner).where(Learner.id == learner_id))
    return _attach_contract(x) if x else None
