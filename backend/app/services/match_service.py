import json,uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.match import MatchResult
from app.schemas.match import MatchCreate
def save(db:Session,p:MatchCreate):
    x=MatchResult(employer_id=p.employer_id,learner_id=p.learner_id,role_title=p.role_title,match_score=p.match_score,matched_skills_json=json.dumps(p.matched_skills),missing_skills_json=json.dumps(p.missing_skills),verified_skills_json=json.dumps(p.verified_skills),explanation=p.explanation);db.add(x);db.commit();db.refresh(x);return x
def learner_matches(db:Session,learner_id:uuid.UUID,limit:int=50):return list(db.scalars(select(MatchResult).where(MatchResult.learner_id==learner_id).order_by(MatchResult.match_score.desc()).limit(limit)).all())
