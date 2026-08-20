import json, uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.verification import MicroProject,Submission,VerificationResult
from app.models.roadmap import RoadmapStep
from app.schemas.verification import MicroProjectCreate,SubmissionCreate
from agents.state import AgentState
from agents.verification_agent import verify_submission

def project(db:Session,p:MicroProjectCreate):
    x=MicroProject(roadmap_step_id=p.roadmap_step_id,skill=p.skill,title=p.title,description=p.description,instructions=p.instructions,language=p.language,difficulty=p.difficulty,rubric_json=json.dumps(p.rubric),test_cases_json=json.dumps(p.test_cases)); db.add(x); db.commit(); db.refresh(x); return x

def submit_and_verify(db:Session,learner, p:SubmissionCreate):
    step=db.get(RoadmapStep,p.node_id)
    if not step: raise ValueError("Roadmap step not found")
    if step.status not in ("unlocked","in_progress"): raise ValueError("Roadmap step is locked")
    x=Submission(project_id=p.project_id or step.id,learner_id=learner.id,code=p.code,language=p.language); db.add(x); db.flush()
    state: AgentState={
        "learner_id":str(learner.id), "target_role": learner.target_role,
        "roadmap":[{"step_id":str(step.id),"skill":step.skill,"title":step.title,"description":step.description,"reason":step.reason,"status":step.status,"citations":json.loads(step.citations_json or "[]")}],
        "active_node_index":0, "active_submission":p.code, "verification_history":[], "retry_count":0, "max_retries":2, "status":"verifying",
    }
    final=verify_submission(state)
    vr=final["verification_history"][-1]
    result=VerificationResult(submission_id=x.id,project_id=uuid.UUID(vr["project_id"]) if _is_uuid(vr["project_id"]) else step.id, learner_id=learner.id,status=vr["status"],score=vr["score"],sandbox_passed=vr["sandbox_passed"],judge_feedback=vr.get("judge_feedback"),llm_feedback=vr.get("llm_feedback"),unlocks_next=vr["unlocks_next"])
    x.status=vr["status"]
    step.status="passed" if vr["unlocks_next"] else ("in_progress" if vr["status"]=="fail" else step.status)
    if vr["unlocks_next"]:
        nxt=db.scalar(select(RoadmapStep).where(RoadmapStep.roadmap_id==step.roadmap_id,RoadmapStep.step_order==step.step_order+1))
        if nxt:nxt.status="unlocked"
        skills=json.loads(learner.verified_skills_json or "[]")
        if step.skill not in skills: skills.append(step.skill)
        learner.verified_skills_json=json.dumps(skills)
    db.add(result); db.commit(); db.refresh(result)
    return _as_read(result)

def _as_read(x):
    x.id=x.id; return x

def _is_uuid(v):
    try: uuid.UUID(str(v)); return True
    except ValueError: return False

def history(db:Session,learner_id:uuid.UUID): return list(db.scalars(select(VerificationResult).where(VerificationResult.learner_id==learner_id).order_by(VerificationResult.verified_at.desc())).all())
