import json, uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.match import MatchResult
from app.models.employer import EmployerRequirement
from app.models.learner import Learner
from matching.service.match_service import EmployerForMatching, LearnerForMatching, MatchingService
from matching.model.matcher import LearnerSkillInput, SkillRequirementInput

def compute_and_save(db: Session, employer_id, requirement: EmployerRequirement, learners: list[Learner], limit: int = 20):
    raw_requirements=json.loads(requirement.required_skills_json or "[]")
    employer=EmployerForMatching(
        employer_id=str(employer_id), role_title=requirement.role_title,
        required_skills=[SkillRequirementInput(skill=x.get("skill", ""), required_level=x.get("required_level", "beginner"), weight=float(x.get("weight",1.0))) for x in raw_requirements],
        description=requirement.description,
    )
    service=MatchingService()
    computed=[]
    for learner in learners:
        profile_skills=json.loads(learner.skills_json or "[]")
        lf=LearnerForMatching(
            learner_id=str(learner.id), target_role=learner.target_role,
            skills=[LearnerSkillInput(skill=(x.get("name","") if isinstance(x,dict) else str(x)), level=(x.get("level","beginner") if isinstance(x,dict) else "beginner")) for x in profile_skills],
            verified_skills=json.loads(learner.verified_skills_json or "[]"),
        )
        computed.append(service.match(lf, employer))
    computed.sort(key=lambda x:x.match_score, reverse=True)
    out=[]
    for x in computed[:limit]:
        row=MatchResult(
            employer_id=uuid.UUID(x.employer_id), learner_id=uuid.UUID(x.learner_id), role_title=x.role_title,
            match_score=x.match_score, matched_skills_json=json.dumps(x.matched_skills), missing_skills_json=json.dumps(x.missing_skills),
            verified_skills_json=json.dumps(x.verified_skills), explanation=x.explanation,
        )
        db.add(row); db.flush()
        row.matched_skills=x.matched_skills; row.missing_skills=x.missing_skills; row.verified_skills=x.verified_skills
        out.append(row)
    db.commit()
    for row in out: db.refresh(row)
    for row in out:
        row.matched_skills=json.loads(row.matched_skills_json); row.missing_skills=json.loads(row.missing_skills_json); row.verified_skills=json.loads(row.verified_skills_json)
    return out

def learner_matches(db:Session,learner_id:uuid.UUID,limit:int=50):
    rows=list(db.scalars(select(MatchResult).where(MatchResult.learner_id==learner_id).order_by(MatchResult.match_score.desc()).limit(limit)).all())
    for x in rows:
        x.matched_skills=json.loads(x.matched_skills_json or "[]"); x.missing_skills=json.loads(x.missing_skills_json or "[]"); x.verified_skills=json.loads(x.verified_skills_json or "[]")
    return rows
