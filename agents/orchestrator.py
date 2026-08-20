"""
agents/orchestrator.py

The LangGraph workflow that owns the diagnose -> plan -> verify flow
described in the proposal's Agent Workflow (section 3.2):

    diagnose -> build_roadmap -> verify_submission --(fail, retries left)--> verify_submission
                                        |
                                        +--(pass, more nodes)--> verify_submission
                                        |
                                        +--(pass, roadmap done)--> END
                                        |
                                        +--(fail, retries exhausted)--> END
"""

import logging
from langgraph.graph import StateGraph, END

from .state import AgentState
from .diagnosis_agent import diagnose
from .roadmap_agent import build_roadmap
from .verification_agent import verify_submission

logger = logging.getLogger(__name__)


def _route_after_verification(state: AgentState) -> str:
    status = state.get("status")
    if status == "completed" or status == "failed":
        return "end"
    return "verify"  # more nodes to go, or awaiting re-submission


def build_graph():
    """Compile the LangGraph StateGraph. Call once at process startup."""
    graph = StateGraph(AgentState)

    graph.add_node("diagnose", diagnose)
    graph.add_node("plan", build_roadmap)
    graph.add_node("verify", verify_submission)

    graph.set_entry_point("diagnose")
    graph.add_edge("diagnose", "plan")
    graph.add_edge("plan", "verify")

    graph.add_conditional_edges(
        "verify",
        _route_after_verification,
        {"verify": "verify", "end": END},
    )

    return graph.compile()


_compiled_graph = None


def run_pipeline(initial_state: AgentState) -> AgentState:
    """
    Entry point used by the FastAPI backend. Runs diagnosis + roadmap
    generation in one pass; the graph then pauses in "verify" state
    between learner submissions (call again with active_submission set
    once the learner submits their micro-project).
    """
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()

    initial_state.setdefault("status", "diagnosing")
    initial_state.setdefault("verification_history", [])
    initial_state.setdefault("retry_count", 0)

    try:
        return _compiled_graph.invoke(initial_state)
    except Exception as e:
        logger.error(f"LangGraph execution exception: {e}")
        initial_state["status"] = "failed"
        initial_state["error"] = str(e)
        return initial_state
