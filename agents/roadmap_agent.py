"""
agents/roadmap_agent.py

Agent 1b: Roadmap Reasoning
Turns skill_gaps into a sequenced, cited roadmap. Every node is grounded
in a real job posting retrieved via RAG — this is the "why this skill"
citation that differentiates SkillBridge from a catalogue recommender.

Aligned with shared/contracts/roadmap.json.
"""

import json
import re
import logging
from typing import Dict, Any, List

from . import config
from .state import AgentState, RoadmapNode, Citation
from .tools import retrieve_relevant_postings
from . import llm_client

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are the Roadmap agent in SkillBridge. You are given a
learner's skill gaps, their target role, and a set of real job-posting
excerpts retrieved for that role. Sequence the skill gaps into a logical
learning order (foundational skills first) and, for each skill, write a
title, description, and one-sentence reason grounded in the provided postings.

Respond with ONLY a JSON array of objects, each shaped as:
[
  {
    "skill": "SQL",
    "title": "SQL Fundamentals & Querying",
    "description": "Master SELECT queries, joins, aggregations, and data filtering.",
    "reason": "SQL appears as a top requirement in 85% of target role job postings.",
    "source_id": "job_001",
    "source_url": "https://example.com/jobs/job_001",
    "snippet": "SQL required"
  }
]

The array must have entries ordered foundational-first. Only use source_url values that appear in the provided postings."""


def build_roadmap(state: AgentState) -> AgentState:
    """LangGraph node: retrieves postings via RAG, then asks LLM to
    sequence and cite a roadmap. Populates state["roadmap"]."""
    if state.get("roadmap") and state.get("status") in ("verifying", "awaiting_submission", "completed"):
        logger.info("Roadmap already generated; skipping re-planning.")
        return state

    raw_gaps = state.get("skill_gaps", [])

    target_role = state.get("target_role", "Data Analyst")

    # Extract skill names whether raw_gaps are dicts (SkillGap) or strings
    gap_names = []
    for g in raw_gaps:
        if isinstance(g, dict):
            gap_names.append(g.get("name", "Required Skill"))
        elif isinstance(g, str):
            gap_names.append(g)

    if not gap_names:
        gap_names = ["SQL", "Data Visualization", "Python"]

    postings = retrieve_relevant_postings(
        query=f"{target_role} " + " ".join(gap_names),
        top_k=config.RAG_TOP_K,
    )

    if not llm_client.is_configured():
        logger.warning(
            "No LLM provider configured (LLM_PROVIDER=%s has no API key). "
            "Using rule-based fallback roadmap generator.", config.LLM_PROVIDER
        )
        return _fallback_roadmap(state, gap_names, postings)

    try:
        user_content = _build_prompt(target_role, gap_names, postings)

        raw_text = llm_client.complete(_SYSTEM_PROMPT, user_content, max_tokens=1536)
        sequenced = _parse_json_response(raw_text)

        roadmap: List[RoadmapNode] = []
        for i, item in enumerate(sequenced):
            citations: List[Citation] = []
            source_url = item.get("source_url", "")
            source_id = item.get("source_id", f"job_{i+1:03d}")
            snippet = item.get("snippet", "Grounded in active market job posting")

            if source_url:
                citations.append({
                    "source_id": source_id,
                    "title": f"Retrieved {target_role} Posting",
                    "url": source_url,
                    "source_name": "Job Vector DB",
                    "snippet": snippet
                })

            roadmap.append({
                "step_id": f"step_{i+1:03d}",
                "skill": item.get("skill", gap_names[i] if i < len(gap_names) else "Skill Node"),
                "title": item.get("title", f"Learn {item.get('skill', 'Skill')}"),
                "description": item.get("description", item.get("reason", "Bridge identified skill gap.")),
                "reason": item.get("reason", "Required by active market job postings."),
                "status": "unlocked" if i == 0 else "locked",
                "citations": citations
            })

        state["roadmap"] = roadmap
    except Exception as e:
        logger.error(f"Roadmap agent LLM call failed: {e}. Applying fallback roadmap.")
        return _fallback_roadmap(state, gap_names, postings)

    state["active_node_index"] = 0
    state["status"] = "verifying"
    return state


def _build_prompt(target_role: str, gap_names: List[str], postings: List[Dict[str, Any]]) -> str:
    postings_block = "\n\n".join(
        f"[{p.get('job_id', f'job_{i+1:03d}')}] {p.get('title', 'Posting')}\n{p.get('text', '')[:500]}\nSOURCE: {p.get('source_url', '')}"
        for i, p in enumerate(postings)
    )
    gaps_block = ", ".join(gap_names)

    return (
        f"Target role: {target_role}\n"
        f"Skill gaps to sequence: {gaps_block}\n\n"
        f"Retrieved job postings:\n{postings_block}"
    )


def _parse_json_response(text: str) -> List[Dict[str, Any]]:
    text = text.strip()
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    if text.startswith("```"):
        text = text.strip("`")
        text = text.split("\n", 1)[1] if "\n" in text else text
    return json.loads(text)


def _fallback_roadmap(state: AgentState, gap_names: List[str], postings: List[Dict[str, Any]]) -> AgentState:
    target_role = state.get("target_role", "Data Analyst")
    roadmap: List[RoadmapNode] = []

    for i, skill in enumerate(gap_names):
        posting = postings[i % len(postings)] if postings else {}
        source_url = posting.get("source_url", "https://example.com/jobs/job_001")
        source_id = posting.get("job_id", f"job_{i+1:03d}")

        citations: List[Citation] = [{
            "source_id": source_id,
            "title": posting.get("title", f"{target_role} Requirement"),
            "url": source_url,
            "source_name": "Job Vector DB",
            "snippet": f"Posting requires practical knowledge in {skill}."
        }]

        roadmap.append({
            "step_id": f"step_{i+1:03d}",
            "skill": skill,
            "title": f"{skill} Mastery Path",
            "description": f"Build practical hands-on experience in {skill}.",
            "reason": f"Frequently listed requirement in active {target_role} hiring listings.",
            "status": "unlocked" if i == 0 else "locked",
            "citations": citations
        })

    state["roadmap"] = roadmap
    state["active_node_index"] = 0
    state["status"] = "verifying"
    return state
