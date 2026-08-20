import logging

from fastapi import APIRouter, HTTPException

from app.schemas.diagnosis import DiagnosisRequest, DiagnosisResponse
from app.services.diagnosis_service import run_diagnosis_pipeline

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])


@router.post("", response_model=DiagnosisResponse)
def create_diagnosis(payload: DiagnosisRequest) -> DiagnosisResponse:
    if not payload.resume_text and not payload.mcq_answers:
        raise HTTPException(400, "Provide resume_text or mcq_answers")

    final_state = run_diagnosis_pipeline(
        target_role=payload.target_role,
        resume_text=payload.resume_text,
        mcq_answers=payload.mcq_answers,
        learner_id=payload.learner_id or "anonymous",
    )

    if final_state.get("status") == "failed":
        logger.error("Diagnosis pipeline failed: %s", final_state.get("error"))
        raise HTTPException(502, "Diagnosis pipeline failed. Please try again.")

    return DiagnosisResponse(
        target_role=payload.target_role,
        current_skills=final_state.get("current_skills", []),
        skill_gaps=final_state.get("skill_gaps", []),
        diagnosis_summary=final_state.get("diagnosis_summary", ""),
        confidence=final_state.get("confidence", 0.0),
        roadmap=final_state.get("roadmap", []),
    )
