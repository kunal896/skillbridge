import json,uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.verification import MicroProject,Submission,VerificationResult
from app.schemas.verification import MicroProjectCreate,SubmissionCreate,VerificationResultCreate
def project(db:Session,p:MicroProjectCreate):
    x=MicroProject(roadmap_step_id=p.roadmap_step_id,skill=p.skill,title=p.title,description=p.description,instructions=p.instructions,language=p.language,difficulty=p.difficulty,rubric_json=json.dumps(p.rubric),test_cases_json=json.dumps(p.test_cases)); db.add(x); db.commit(); db.refresh(x); return x
def submit(db:Session,learner_id:uuid.UUID,p:SubmissionCreate):
    x=Submission(project_id=p.project_id,learner_id=learner_id,code=p.code,language=p.language); db.add(x); db.commit(); db.refresh(x); return x
def result(db:Session,learner_id:uuid.UUID,p:VerificationResultCreate):
    x=VerificationResult(submission_id=p.submission_id,project_id=p.project_id,learner_id=learner_id,status=p.status,score=p.score,sandbox_passed=p.sandbox_passed,judge_feedback=p.judge_feedback,llm_feedback=p.llm_feedback,unlocks_next=p.unlocks_next); db.add(x); db.commit(); db.refresh(x); return x
def history(db:Session,learner_id:uuid.UUID): return list(db.scalars(select(VerificationResult).where(VerificationResult.learner_id==learner_id).order_by(VerificationResult.verified_at.desc())).all())
