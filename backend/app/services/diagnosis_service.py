"""
app/services/diagnosis_service.py

Thin bridge between the FastAPI backend and the agents/ LangGraph
pipeline. Keeps agents.orchestrator.run_pipeline as the single entry
point both the CLI (agents/main.py) and the API use, so the two never
drift into separate implementations of the same diagnose -> plan flow.
"""

from typing import Any, Dict, Optional

from agents.orchestrator import run_pipeline


def run_diagnosis_pipeline(
    target_role: str,
    resume_text: Optional[str] = None,
    mcq_answers: Optional[Dict[str, str]] = None,
    learner_id: str = "anonymous",
) -> Dict[str, Any]:
    """Runs diagnose -> plan for one learner and returns the final agent state."""
    initial_state: Dict[str, Any] = {
        "learner_id": learner_id,
        "target_role": target_role,
    }
    if resume_text:
        initial_state["resume_text"] = resume_text
    if mcq_answers:
        initial_state["mcq_answers"] = mcq_answers

    return run_pipeline(initial_state)
