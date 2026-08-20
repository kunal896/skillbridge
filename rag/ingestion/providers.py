"""
rag/ingestion/providers.py

Fetches raw job postings for ingestion. Live Adzuna API when
ADZUNA_APP_ID / ADZUNA_APP_KEY are configured, otherwise the bundled
offline sample dataset (rag/ingestion/sample_postings.py) filtered to
the requested query -- this is what agents/tools.py used to do inline
with only 3 hardcoded postings; it's now a real, swappable ingestion
source that rag/ owns.
"""

import logging
from typing import Any, Dict, List

import requests

from .. import config
from .sample_postings import SAMPLE_POSTINGS

logger = logging.getLogger(__name__)


def fetch_postings(query: str, region: str = None, limit: int = 25) -> List[Dict[str, Any]]:
    """Fetch raw (not-yet-normalized) postings for `query`."""
    region = region or config.ADZUNA_COUNTRY

    if config.JOB_DATA_PROVIDER == "adzuna" and config.ADZUNA_APP_ID and config.ADZUNA_APP_KEY:
        try:
            return _fetch_from_adzuna(query, region, limit)
        except Exception as e:
            logger.error(f"Adzuna fetch failed: {e}. Falling back to sample dataset.")
            return _fetch_from_sample(query, limit)

    if config.JOB_DATA_PROVIDER == "adzuna":
        logger.info("Adzuna API credentials not configured; using bundled sample dataset.")

    return _fetch_from_sample(query, limit)


def _fetch_from_adzuna(query: str, region: str, limit: int) -> List[Dict[str, Any]]:
    url = f"https://api.adzuna.com/v1/api/jobs/{region.lower()}/search/1"
    params = {
        "app_id": config.ADZUNA_APP_ID,
        "app_key": config.ADZUNA_APP_KEY,
        "results_per_page": limit,
        "what": query,
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    for r in results:
        r["source_name"] = "Adzuna"
    return results


def _fetch_from_sample(query: str, limit: int) -> List[Dict[str, Any]]:
    """Returns sample postings, preferring ones whose role_family matches
    the query so ingesting per target-role still produces relevant data."""
    query_lower = query.lower()
    matching = [p for p in SAMPLE_POSTINGS if p["role_family"].lower() in query_lower or any(
        word in query_lower for word in p["role_family"].lower().split()
    )]
    ordered = matching + [p for p in SAMPLE_POSTINGS if p not in matching]
    return ordered[:limit]
