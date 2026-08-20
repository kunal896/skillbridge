"""
agents/config.py

Central place for environment-driven configuration. Never hardcode
secrets here — everything is read from the environment so the same
code works locally (.env) and in deployment (Render/AWS secrets).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# ---- LLM ----
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")

# ---- Vector store (job postings RAG index) ----
VECTOR_STORE_BACKEND = os.environ.get("VECTOR_STORE_BACKEND", "chroma")  # "chroma" | "pinecone"
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "./data/chroma")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "skillbridge-job-postings")

# ---- Job data ingestion ----
JOB_DATA_PROVIDER = os.environ.get("JOB_DATA_PROVIDER", "adzuna")  # "adzuna" | "jooble"
ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.environ.get("ADZUNA_APP_KEY", "")

# ---- Judge0 sandbox ----
JUDGE0_BASE_URL = os.environ.get("JUDGE0_BASE_URL", "http://localhost:2358")
JUDGE0_API_KEY = os.environ.get("JUDGE0_API_KEY", "")

# ---- Database ----
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://skillbridge:skillbridge@localhost:5432/skillbridge")

# ---- Agent behavior ----
DEFAULT_MAX_RETRIES = int(os.environ.get("DEFAULT_MAX_RETRIES", "2"))
ROADMAP_LENGTH = int(os.environ.get("ROADMAP_LENGTH", "6"))
RAG_TOP_K = int(os.environ.get("RAG_TOP_K", "5"))
