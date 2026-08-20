"""
rag/ingestion/run_ingest.py

Offline ingestion pipeline: fetch postings for a set of target roles,
normalize them into the canonical JobPosting shape, and upsert them
into the configured vector store.

Run directly:
    python -m rag.ingestion.run_ingest
    python -m rag.ingestion.run_ingest --roles "Data Analyst" "Backend Engineer"

Or import and call from elsewhere (e.g. a scheduled backend job):
    from rag.ingestion.run_ingest import ingest
    ingest(["Data Analyst"])
"""

import argparse
import logging
from typing import List

from .. import config
from ..normalization.normalize import normalize_postings
from .providers import fetch_postings

logger = logging.getLogger(__name__)


def ingest(roles: List[str] = None, limit_per_role: int = 25) -> int:
    """Fetch, normalize, and upsert postings for each role. Returns the
    total number of postings written."""
    roles = roles or config.SAMPLE_DATASET_ROLES

    if config.VECTOR_STORE_BACKEND != "chroma":
        raise RuntimeError(
            f"Ingestion currently only writes to the chroma backend "
            f"(VECTOR_STORE_BACKEND={config.VECTOR_STORE_BACKEND!r}). "
            f"Pinecone upsert isn't wired yet -- see rag/vectorstore/pinecone_store.py."
        )

    from ..vectorstore.chroma_store import ChromaJobStore
    store = ChromaJobStore()

    total_written = 0
    for role in roles:
        logger.info(f"Fetching postings for '{role}'...")
        raw = fetch_postings(role, limit=limit_per_role)
        normalized = normalize_postings(raw)
        written = store.upsert(normalized)
        logger.info(f"  -> normalized {len(normalized)}/{len(raw)}, wrote {written} to '{store.collection_name}'")
        total_written += written

    logger.info(f"Ingestion complete. {total_written} postings written. Collection size: {store.count()}")
    return total_written


def main():
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = argparse.ArgumentParser(description="Ingest job postings into the RAG vector store")
    parser.add_argument(
        "--roles",
        nargs="+",
        default=None,
        help="Target roles to ingest postings for (default: rag.config.SAMPLE_DATASET_ROLES)",
    )
    parser.add_argument("--limit", type=int, default=25, help="Max postings to fetch per role")
    args = parser.parse_args()

    ingest(roles=args.roles, limit_per_role=args.limit)


if __name__ == "__main__":
    main()
