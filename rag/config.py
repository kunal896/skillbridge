"""
rag/config.py

Central place for rag/'s own environment-driven configuration. rag/ is
consumed by agents/ (and could be consumed by backend/ directly for an
admin ingestion endpoint) but must not import from either -- it reads
its own environment the same way agents/config.py does.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load the repo-root .env if present (same file agents/ and backend/ use),
# so a single `.env` at the project root configures every module.
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)
else:
    load_dotenv()

# ---- Vector store ----
VECTOR_STORE_BACKEND = os.environ.get("VECTOR_STORE_BACKEND", "chroma")  # "chroma" | "pinecone"
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "./data/chroma")
CHROMA_COLLECTION_NAME = os.environ.get("CHROMA_COLLECTION_NAME", "job_postings")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "skillbridge-job-postings")

# ---- Job data ingestion ----
JOB_DATA_PROVIDER = os.environ.get("JOB_DATA_PROVIDER", "adzuna")  # "adzuna" | "sample"
ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY", "")
ADZUNA_COUNTRY = os.environ.get("ADZUNA_COUNTRY", "in")

# ---- Retrieval ----
RAG_TOP_K = int(os.environ.get("RAG_TOP_K", "5"))

# Roles the bundled sample dataset (rag/ingestion/sample_postings.py)
# covers. Used as the offline/no-API-key fallback so retrieval still
# varies meaningfully by target role instead of always returning the
# same 3 generic postings.
SAMPLE_DATASET_ROLES = [
    "Data Analyst",
    "Backend Engineer",
    "Frontend Engineer",
    "DevOps Engineer",
    "Machine Learning Engineer",
    "Product Manager",
    "QA Engineer",
    "UI/UX Designer",
]
