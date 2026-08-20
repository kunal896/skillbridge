"""
agents/verification_agent.py

Agent 2: Verification orchestration
For the currently unlocked roadmap node, this agent:
  1. Generates a micro-project spec for that skill (on first entry).
  2. Grades the learner's submission — sandboxed execution (Judge0)
     for coding tasks, plus an LLM-as-judge rubric pass.
  3. Unlocks the next node on pass, or increments retry_count on fail.

A node only unlocks the next one on a verified pass — this is the gate
that makes "in progress" mean something, per the proposal's core claim.
Aligned with shared/contracts/verification.json.
"""

import json
import re
import datetime
import logging
from typing import Dict, Any

from . import config
from .state import AgentState, VerificationResult
from .tools import run_judge0_submission
from . import llm_client

logger = logging.getLogger(__name__)

_JUDGE_SYSTEM_PROMPT = """You are the Verification agent in SkillBridge, acting
as an LLM-as-judge. You are given a target skill, a micro-project spec, the
learner's submitted code, and the sandbox execution result (stdout/stderr).

Grade the submission 0-100 against the spec's rubric and decide pass/fail
(pass threshold is 70).

Respond ONLY with a JSON object:
{
  "score": 85.0,
  "passed": true,
  "judge_feedback": "All core test cases passed. Clean syntax and clear variable naming.",
  "llm_feedback": "Code efficiently handles edge cases."
}"""

PASS_THRESHOLD = 70
PYTHON3_LANGUAGE_ID = 71  # Judge0 language id for Python 3


def generate_micro_project(skill: str) -> str:
    """Produce a short project spec for the given skill node."""
    if not llm_client.is_configured():
        return f"Write a Python script that demonstrates competence in {skill}. Include input validation and clear function output."

    try:
        return llm_client.complete(
            (
                "You are the Verification agent in SkillBridge. Write a short, "
                "concrete coding micro-project spec (3-6 sentences) that verifies "
                "practical competence in the given skill. Include explicit "
                "input/output expectations so it can be auto-graded."
            ),
            f"Skill to verify: {skill}",
            max_tokens=512,
        ).strip()
    except Exception as e:
        logger.error(f"Failed to generate micro-project: {e}")
        return f"Write a Python script that demonstrates competence in {skill}."


def verify_submission(state: AgentState) -> AgentState:
    """LangGraph node: grades state['active_submission'] against the
    active roadmap node, updates roadmap status and retry_count."""

    idx = state.get("active_node_index", 0)
    roadmap = state.get("roadmap", [])

    if not roadmap or idx >= len(roadmap):
        state["status"] = "completed"
        return state

    node = roadmap[idx]
    submission = state.get("active_submission", "")
    learner_id = state.get("learner_id", "demo_learner")

    node["status"] = "in_progress"

    if not submission:
        logger.info("No active submission provided yet. Waiting for learner input.")
        state["status"] = "awaiting_submission"
        return state

    judge0_result = run_judge0_submission(
        source_code=submission,
        language_id=PYTHON3_LANGUAGE_ID,
    )
    stdout = judge0_result.get("stdout", "") or ""
    stderr = judge0_result.get("stderr", "") or judge0_result.get("compile_output", "") or ""

    verdict = _llm_judge(node["skill"], submission, stdout, stderr)

    sandbox_ok = judge0_result.get("status", {}).get("id") == 3
    is_passed = sandbox_ok and verdict.get("passed", False) and verdict.get("score", 0) >= PASS_THRESHOLD

    result: VerificationResult = {
        "project_id": f"proj_{node.get('step_id', idx+1)}",
        "learner_id": learner_id,
        "node_skill": node["skill"],
        "status": "pass" if is_passed else "fail",
        "score": float(verdict.get("score", 0)),
        "sandbox_passed": verdict.get("passed", False),
        "judge_feedback": verdict.get("judge_feedback", verdict.get("feedback", "Evaluation complete.")),
        "llm_feedback": verdict.get("llm_feedback", "Detailed code review completed."),
        "unlocks_next": is_passed,
        "judge0_stdout": stdout,
        "judge0_stderr": stderr,
        "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    state.setdefault("verification_history", []).append(result)

    if is_passed:
        node["status"] = "passed"
        _unlock_next_node(state, idx)
        state["active_submission"] = ""
        state["status"] = "awaiting_submission" if idx + 1 < len(roadmap) else "completed"
    else:
        state["retry_count"] = state.get("retry_count", 0) + 1
        max_retries = state.get("max_retries", config.DEFAULT_MAX_RETRIES)
        if state["retry_count"] > max_retries:
            node["status"] = "failed"
            state["status"] = "failed"
        else:
            state["status"] = "awaiting_submission"

    return state



def _unlock_next_node(state: AgentState, current_idx: int) -> None:
    roadmap = state["roadmap"]
    next_idx = current_idx + 1
    if next_idx < len(roadmap):
        roadmap[next_idx]["status"] = "unlocked"
        state["active_node_index"] = next_idx
        state["retry_count"] = 0


def _llm_judge(skill: str, submission: str, stdout: str, stderr: str) -> Dict[str, Any]:
    if not llm_client.is_configured():
        return {
            "score": 0.0,
            "passed": False,
            "judge_feedback": "LLM judge is not configured; verification cannot be approved.",
            "llm_feedback": "Configure LLM_PROVIDER and its API key before verification.",
        }

    try:
        prompt = (
            f"Skill: {skill}\n\n"
            f"Submitted code:\n{submission}\n\n"
            f"Sandbox stdout:\n{stdout}\n\n"
            f"Sandbox stderr:\n{stderr}"
        )
        raw_text = llm_client.complete(_JUDGE_SYSTEM_PROMPT, prompt, max_tokens=512)
        return _parse_json_response(raw_text)
    except Exception as e:
        logger.error(f"LLM judge evaluation failed: {e}")
        return {
            "score": 0.0,
            "passed": False,
            "judge_feedback": "LLM judge unavailable; verification not approved.",
            "llm_feedback": f"Judge error: {e}",
        }


def _parse_json_response(text: str) -> Dict[str, Any]:
    text = text.strip()
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    if text.startswith("```"):
        text = text.strip("`")
        text = text.split("\n", 1)[1] if "\n" in text else text
    return json.loads(text)
