import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import get_optional_account
from app.db.session import get_db
from app.models.account import Account
from app.models.roadmap import Roadmap
from app.schemas.diagnosis import DiagnosisRequest, DiagnosisResponse
from app.schemas.learner import LearnerCreate, SkillInput
from app.services.diagnosis_service import run_diagnosis_pipeline
from app.services.learner_service import upsert
from app.services.roadmap_service import create_from_agent_roadmap
logger=logging.getLogger(__name__)
router=APIRouter(prefix="/diagnosis",tags=["diagnosis"])

@router.post("",response_model=DiagnosisResponse)
def create_diagnosis(payload:DiagnosisRequest, account:Account|None=Depends(get_optional_account), db:Session=Depends(get_db)):
    if not payload.resume_text and not payload.mcq_answers:
        raise HTTPException(400,"Provide resume_text or mcq_answers")

    learner = None
    if account and account.role == "learner":
        learner = upsert(
            db,
            account.id,
            LearnerCreate(
                target_role=payload.target_role,
                resume_text=payload.resume_text,
                profile_source="resume" if payload.resume_text else "mcq",
            ),
        )
        pipeline_learner_id = str(learner.id)
    else:
        pipeline_learner_id = payload.learner_id or "anonymous"

    final=run_diagnosis_pipeline(
        target_role=payload.target_role,
        resume_text=payload.resume_text,
        mcq_answers=payload.mcq_answers,
        learner_id=pipeline_learner_id,
    )
    if final.get("status")=="failed":
        raise HTTPException(502,"Diagnosis pipeline failed. Please try again.")

    if learner:
        current=[SkillInput(**x) for x in final.get("current_skills",[]) if isinstance(x,dict) and x.get("name")]
        learner=upsert(
            db,
            account.id,
            LearnerCreate(
                target_role=payload.target_role,
                resume_text=payload.resume_text,
                skills=current,
                profile_source="resume" if payload.resume_text else "mcq",
            ),
        )
        if final.get("roadmap"):
            existing=list(db.scalars(select(Roadmap).where(Roadmap.learner_id==learner.id,Roadmap.status=="active")).all())
            for old in existing:
                old.status="archived"
            create_from_agent_roadmap(
                db,
                learner.id,
                payload.target_role,
                final.get("diagnosis_summary"),
                final["roadmap"],
            )

    return DiagnosisResponse(
        learner_id=str(learner.id) if learner else (payload.learner_id or None),
        target_role=payload.target_role,
        current_skills=final.get("current_skills",[]),
        skill_gaps=final.get("skill_gaps",[]),
        diagnosis_summary=final.get("diagnosis_summary",""),
        confidence=final.get("confidence",0.0),
        roadmap=final.get("roadmap",[]),
    )
