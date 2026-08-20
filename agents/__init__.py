"""
agents/
SkillBridge multi-agent package.

Owns:
    - diagnosis            (agents/diagnosis_agent.py)
    - roadmap reasoning     (agents/roadmap_agent.py)
    - verification orchestration (agents/verification_agent.py)
    - LangGraph workflow    (agents/orchestrator.py)

Consumes:
    - learner/job data      (agents/tools.py -> fetch_learner_profile, fetch_job_postings)
    - RAG retrieval          (agents/tools.py -> retrieve_relevant_postings)
    - Judge0 verification    (agents/tools.py -> run_judge0_submission)
"""

from .orchestrator import build_graph, run_pipeline
from .state import AgentState, RoadmapNode, VerificationResult, SkillAssessment, SkillGap, Citation

__all__ = [
    "build_graph",
    "run_pipeline",
    "AgentState",
    "RoadmapNode",
    "VerificationResult",
    "SkillAssessment",
    "SkillGap",
    "Citation"
]
