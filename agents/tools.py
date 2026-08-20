"""
agents/tools.py

Everything the agents/ package *consumes* from the rest of the system:
    - learner/job data   -> fetch_learner_profile, fetch_job_postings
    - RAG retrieval        -> retrieve_relevant_postings
    - Judge0 verification  -> run_judge0_submission

These are thin wrappers so the agent logic (diagnosis_agent.py,
roadmap_agent.py, verification_agent.py) never talks to HTTP/DB
clients directly — swap an implementation here without touching
agent code.
"""

import time
import logging
import requests
from typing import List, Dict, Any

from . import config

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Learner / job data
# --------------------------------------------------------------------------

def fetch_learner_profile(learner_id: str) -> Dict[str, Any]:
    """
    Pull a learner's stored profile (resume text, prior MCQ answers,
    target role) from the backend API / Postgres ledger.
    """
    # Stub implementation until FastAPI endpoint is running
    return {
        "learner_id": learner_id,
        "target_role": "Data Analyst",
        "resume_text": "Experienced in Excel reporting, SQL basics, and python script writing.",
        "skills": ["Excel", "Basic SQL"]
    }


def fetch_job_postings(query: str, region: str = "IN", limit: int = 25) -> List[Dict[str, Any]]:
    """
    Pull fresh job postings from the configured provider (Adzuna/Jooble)
    for ingestion into the vector store. Used by the offline ingestion
    pipeline.
    """
    if config.JOB_DATA_PROVIDER == "adzuna":
        if not config.ADZUNA_APP_ID or not config.ADZUNA_APP_KEY:
            logger.warning("Adzuna API credentials not configured, returning mock job postings.")
            return _get_mock_job_postings(query)

        url = f"https://api.adzuna.com/v1/api/jobs/{region.lower()}/search/1"
        params = {
            "app_id": config.ADZUNA_APP_ID,
            "app_key": config.ADZUNA_APP_KEY,
            "results_per_page": limit,
            "what": query,
        }
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except Exception as e:
            logger.error(f"Adzuna fetch failed: {e}")
            return _get_mock_job_postings(query)

    return _get_mock_job_postings(query)


# --------------------------------------------------------------------------
# RAG retrieval over the job-postings vector store
# --------------------------------------------------------------------------

def retrieve_relevant_postings(query: str, top_k: int = None) -> List[Dict[str, Any]]:
    """Single RAG boundary. Agents never implement vector-store logic."""
    from rag.retrieval import retrieve_postings
    return retrieve_postings(query, top_k or config.RAG_TOP_K)


# --------------------------------------------------------------------------
# Judge0 sandboxed execution (verification agent)
# --------------------------------------------------------------------------

def run_judge0_submission(source_code: str, language_id: int = 71, stdin: str = "") -> Dict[str, Any]:
    """
    Submit code to Judge0 for sandboxed execution and poll for the result.
    language_id follows Judge0's language table (e.g. 71 = Python 3).
    """
    if not source_code:
        return {"stdout": "", "stderr": "No source code provided", "status": {"id": 6, "description": "Compilation Error"}}

    headers = {"Content-Type": "application/json"}
    if config.JUDGE0_API_KEY:
        headers["X-RapidAPI-Key"] = config.JUDGE0_API_KEY

    try:
        submit_resp = requests.post(
            f"{config.JUDGE0_BASE_URL}/submissions?base64_encoded=false&wait=false",
            json={"source_code": source_code, "language_id": language_id, "stdin": stdin},
            headers=headers,
            timeout=10,
        )
        submit_resp.raise_for_status()
        token = submit_resp.json()["token"]

        # Poll until judged
        for _ in range(15):
            result_resp = requests.get(
                f"{config.JUDGE0_BASE_URL}/submissions/{token}",
                headers=headers,
                timeout=10,
            )
            result_resp.raise_for_status()
            data = result_resp.json()
            if data.get("status", {}).get("id", 0) >= 3:  # 3 = finished (any terminal state)
                return data
            time.sleep(1)

        return {"stdout": "", "stderr": "Judge0 execution timed out", "status": {"id": 5, "description": "Time Limit Exceeded"}}
    except Exception as e:
        logger.error("Judge0 connection unavailable: %s", e)
        return {
            "stdout": "",
            "stderr": f"Judge0 unavailable: {e}",
            "status": {"id": -1, "description": "Judge0 Unavailable"}
        }
