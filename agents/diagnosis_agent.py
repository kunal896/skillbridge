"""
agents/diagnosis_agent.py

Agent 1a: Diagnosis
Extracts a learner's current skills from a resume and/or MCQ answers,
then computes the skill gap against their target role.

This is NLP + ML classification, not a free-form chatbot turn: the
output is a structured list of skills so downstream agents can reason
over it deterministically. Aligned with shared/contracts/diagnosis.json.
"""

import json
import re
import logging
from typing import Dict, Any, List

from . import config
from .state import AgentState, SkillAssessment, SkillGap

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are the Diagnosis agent in SkillBridge, an AI reskilling platform.
Given a learner's resume text and/or MCQ answers, and their target role, analyze their current skills and identify their skill gaps.

Extract two things:
1. current_skills: a list of objects {"name": str, "level": "beginner"|"intermediate"|"advanced", "evidence": [str]}
2. skill_gaps: a list of objects {"name": str, "priority": int (1=highest), "reason": str, "evidence_job_ids": []}

Be concrete and use industry-standard skill names (e.g. "SQL", "Excel", "Python", "Data Analysis"), not vague categories.
Also provide "diagnosis_summary" (str) and "confidence" (number between 0.0 and 1.0).

Respond ONLY with a valid JSON object:
{
  "current_skills": [
    {"name": "Excel", "level": "intermediate", "evidence": ["2 years reporting experience"]}
  ],
  "skill_gaps": [
    {"name": "SQL", "priority": 1, "reason": "High demand in target role postings", "evidence_job_ids": []}
  ],
  "diagnosis_summary": "Strong spreadsheet background; SQL and Python are key gaps.",
  "confidence": 0.90
}"""


def diagnose(state: AgentState) -> AgentState:
    """LangGraph node: populates current_skills, skill_gaps, diagnosis_summary, confidence on the state."""
    user_content = _build_prompt(state)

    if not config.ANTHROPIC_API_KEY:
        logger.warning("ANTHROPIC_API_KEY not set. Using rule-based fallback diagnosis.")
        return _fallback_diagnosis(state)

    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1024,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )

        parsed = _parse_json_response(response.content[0].text)

        state["current_skills"] = parsed.get("current_skills", [])
        state["skill_gaps"] = parsed.get("skill_gaps", [])
        state["diagnosis_summary"] = parsed.get("diagnosis_summary", "Skill gap diagnosis complete.")
        state["confidence"] = parsed.get("confidence", 0.85)
    except Exception as e:
        logger.error(f"Diagnosis agent LLM call failed: {e}. Applying fallback diagnosis.")
        return _fallback_diagnosis(state)

    state["status"] = "planning"
    return state


def _build_prompt(state: AgentState) -> str:
    parts = [f"Target role: {state.get('target_role', 'Data Analyst')}"]

    if state.get("resume_text"):
        parts.append(f"Resume:\n{state['resume_text']}")

    if state.get("mcq_answers"):
        answers = "\n".join(f"- {q}: {a}" for q, a in state["mcq_answers"].items())
        parts.append(f"MCQ skill-check answers:\n{answers}")

    return "\n\n".join(parts)


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


def _fallback_diagnosis(state: AgentState) -> AgentState:
    target_role = state.get("target_role", "Data Analyst")
    resume = state.get("resume_text", "").lower()
    
    current_skills: List[SkillAssessment] = []
    skill_gaps: List[SkillGap] = []

    if "excel" in resume or "spreadsheet" in resume:
        current_skills.append({"name": "Excel", "level": "intermediate", "evidence": ["Mentioned in resume"]})
    else:
        skill_gaps.append({"name": "Excel & Spreadsheets", "priority": 3, "reason": "Fundamental data entry and reporting", "evidence_job_ids": ["job_001"]})

    if "sql" in resume or "database" in resume:
        current_skills.append({"name": "SQL", "level": "intermediate", "evidence": ["Mentioned in resume"]})
    else:
        skill_gaps.append({"name": "SQL", "priority": 1, "reason": "High frequency requirement in target postings", "evidence_job_ids": ["job_001", "job_002"]})

    if "python" in resume or "pandas" in resume:
        current_skills.append({"name": "Python", "level": "beginner", "evidence": ["Mentioned in resume"]})
    else:
        skill_gaps.append({"name": "Python", "priority": 2, "reason": "Required for automated data analysis and ETL", "evidence_job_ids": ["job_003"]})

    if not current_skills:
        current_skills.append({"name": "General Analytics", "level": "beginner", "evidence": ["Self-reported interest"]})

    state["current_skills"] = current_skills
    state["skill_gaps"] = skill_gaps
    state["diagnosis_summary"] = f"Diagnosed {len(skill_gaps)} skill gaps for target role {target_role}."
    state["confidence"] = 0.80
    state["status"] = "planning"
    return state
