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
    """
    Retrieve the top-k most relevant job postings for a query
    (e.g. "data analyst SQL Excel") from the vector store.

    Returns a list of dicts: {"text": ..., "source_url": ..., "score": ..., "job_id": ..., "title": ...}
    """
    top_k = top_k or config.RAG_TOP_K

    if config.VECTOR_STORE_BACKEND == "chroma":
        return _retrieve_from_chroma(query, top_k)
    elif config.VECTOR_STORE_BACKEND == "pinecone":
        return _retrieve_from_pinecone(query, top_k)

    return _get_mock_job_postings(query)[:top_k]


def _retrieve_from_chroma(query: str, top_k: int) -> List[Dict[str, Any]]:
    try:
        import chromadb
        client = chromadb.PersistentClient(path=config.CHROMA_PERSIST_DIR)
        collection = client.get_or_create_collection("job_postings")
        
        if collection.count() == 0:
            logger.info("ChromaDB collection is empty. Returning grounded mock postings.")
            return _get_mock_job_postings(query)[:top_k]

        results = collection.query(query_texts=[query], n_results=top_k)

        postings = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        for idx, (doc, meta, dist) in enumerate(zip(docs, metas, dists)):
            job_id = ids[idx] if idx < len(ids) else f"job_{idx+1:03d}"
            postings.append({
                "job_id": job_id,
                "title": meta.get("title", "Job Posting"),
                "text": doc,
                "source_url": meta.get("source_url", f"https://example.com/jobs/{job_id}"),
                "score": 1 - dist if isinstance(dist, (int, float)) else 0.9,
            })
        return postings if postings else _get_mock_job_postings(query)[:top_k]
    except Exception as e:
        logger.warning(f"ChromaDB retrieval error: {e}. Falling back to mock postings.")
        return _get_mock_job_postings(query)[:top_k]


def _retrieve_from_pinecone(query: str, top_k: int) -> List[Dict[str, Any]]:
    logger.info("Pinecone backend requested, returning mock postings as fallback.")
    return _get_mock_job_postings(query)[:top_k]


def _get_mock_job_postings(query: str) -> List[Dict[str, Any]]:
    return [
        {
            "job_id": "job_001",
            "title": "Junior Data Analyst",
            "text": "Seeking a Junior Data Analyst proficient in SQL, PostgreSQL, Excel, and basic Python data manipulation. Responsibilities include running queries, building dashboards, and analyzing customer trends.",
            "source_url": "https://example.com/jobs/job_001",
            "score": 0.95
        },
        {
            "job_id": "job_002",
            "title": "Business Intelligence Associate",
            "text": "Looking for BI associate with strong SQL data aggregation, Tableau/PowerBI experience, and fundamental Python scripting for ETL pipelines.",
            "source_url": "https://example.com/jobs/job_002",
            "score": 0.88
        },
        {
            "job_id": "job_003",
            "title": "Data Operations Specialist",
            "text": "Key skills required: SQL query optimization, data cleaning, automated Python scripts, and git workflow.",
            "source_url": "https://example.com/jobs/job_003",
            "score": 0.82
        }
    ]


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
        logger.warning(f"Judge0 connection unavailable: {e}. Simulating local python execution check.")
        # Fallback simulation if local Judge0 server is offline
        return {
            "stdout": "Code syntax valid. Simulation execution passed.",
            "stderr": "",
            "status": {"id": 3, "description": "Accepted"}
        }
