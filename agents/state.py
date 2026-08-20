"""
agents/state.py

Shared state object passed between nodes in the LangGraph workflow:
Diagnosis -> Roadmap -> Verification (loops back to Verification until
each node in the roadmap is either passed or exhausts its retry budget).

Aligned with shared/contracts/ JSON schemas.
"""

from typing import TypedDict, List, Dict, Optional, Literal, Any


class SkillAssessment(TypedDict, total=False):
    name: str
    level: str  # "beginner" | "intermediate" | "advanced"
    evidence: List[str]


class SkillGap(TypedDict, total=False):
    name: str
    priority: int
    reason: str
    evidence_job_ids: List[str]


class Citation(TypedDict, total=False):
    source_id: str
    title: str
    url: str
    source_name: str
    snippet: str


class RoadmapNode(TypedDict, total=False):
    step_id: str
    skill: str
    title: str
    description: str
    reason: str
    status: Literal["locked", "unlocked", "in_progress", "passed", "failed"]
    citations: List[Citation]


class VerificationResult(TypedDict, total=False):
    project_id: str
    learner_id: str
    node_skill: str
    status: Literal["pass", "fail", "error"]
    score: float  # 0-100
    sandbox_passed: bool
    judge_feedback: str
    llm_feedback: str
    unlocks_next: bool
    judge0_stdout: Optional[str]
    judge0_stderr: Optional[str]
    verified_at: str


class AgentState(TypedDict, total=False):
    # ---- Input ----
    learner_id: str
    resume_text: Optional[str]
    mcq_answers: Optional[Dict[str, str]]
    target_role: str

    # ---- Diagnosis Agent Output ----
    current_skills: List[Any]  # list of SkillAssessment dicts or strings
    skill_gaps: List[Any]      # list of SkillGap dicts or strings
    diagnosis_summary: str
    confidence: float

    # ---- Roadmap Agent Output ----
    roadmap: List[RoadmapNode]
    active_node_index: int

    # ---- Verification Agent Output ----
    active_submission: Optional[str]     # learner's code / project submission
    verification_history: List[VerificationResult]
    retry_count: int
    max_retries: int

    # ---- Control ----
    status: Literal[
        "diagnosing", "planning", "verifying", "completed", "failed"
    ]
    error: Optional[str]
