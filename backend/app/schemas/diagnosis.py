from pydantic import BaseModel


class DiagnosisRequest(BaseModel):
    target_role: str
    resume_text: str | None = None
    mcq_answers: dict[str, str] | None = None
    # Optional — lets an authenticated caller associate the run with a
    # learner without requiring it (anonymous/onboarding-time diagnosis
    # is a first-class use case, not just a logged-in feature).
    learner_id: str | None = None


class DiagnosisResponse(BaseModel):
    target_role: str
    current_skills: list[dict]
    skill_gaps: list[dict]
    diagnosis_summary: str
    confidence: float
    # The pipeline runs diagnose -> plan in one pass (see
    # agents/orchestrator.py), so the cited roadmap comes back alongside
    # the diagnosis instead of requiring a second round trip.
    roadmap: list[dict]
