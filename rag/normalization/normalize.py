"""
rag/normalization/normalize.py

Normalizes raw postings from any ingestion source (Adzuna API response,
bundled sample dataset, future providers) into the canonical JobPosting
shape defined by shared/contracts/job_posting.json. Everything
downstream (embeddings, vectorstore, retrieval, citations) works off
this one normalized shape so it doesn't need to know which provider a
posting came from.
"""

import datetime
import re
from typing import Any, Dict, List, Optional

# A small, extensible skill vocabulary used for lightweight keyword
# tagging when a provider doesn't supply structured skill tags itself
# (Adzuna doesn't; our bundled sample dataset doesn't either). This is
# intentionally simple -- it's a normalization aid, not a classifier.
_SKILL_VOCAB = [
    "SQL", "Excel", "Python", "Pandas", "NumPy", "PowerBI", "Tableau",
    "PostgreSQL", "MySQL", "MongoDB", "ETL", "Docker", "Kubernetes",
    "Terraform", "Ansible", "AWS", "GCP", "Azure", "React", "TypeScript",
    "JavaScript", "Next.js", "Tailwind CSS", "HTML", "CSS", "FastAPI",
    "Django", "REST API", "GraphQL", "Kafka", "RabbitMQ", "CI/CD",
    "Git", "PyTorch", "scikit-learn", "TensorFlow", "LLM", "Figma",
    "Selenium", "Playwright", "JWT", "OAuth2", "Prometheus", "Grafana",
]


def _extract_skills(text: str) -> List[str]:
    found = []
    lowered = text.lower()
    for skill in _SKILL_VOCAB:
        if re.search(r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])", lowered):
            found.append(skill)
    return found


def normalize_posting(raw: Dict[str, Any], source_name: str = "sample") -> Optional[Dict[str, Any]]:
    """Normalize one raw posting dict into the canonical JobPosting shape.
    Returns None if the posting is missing the minimum required fields
    (job_id, title, description text) rather than raising, since
    ingestion should skip malformed records instead of aborting a whole
    batch."""
    job_id = raw.get("job_id") or raw.get("id")
    title = raw.get("title")
    description = raw.get("text") or raw.get("description")

    if not job_id or not title or not description:
        return None

    company = raw.get("company")
    if isinstance(company, dict):
        company = company.get("display_name")

    location = raw.get("location")
    if isinstance(location, dict):
        location = location.get("display_name")

    return {
        "job_id": str(job_id),
        "title": title,
        "company": company,
        "location": location,
        "region": raw.get("region") or raw.get("role_family"),
        "description": description,
        "skills": raw.get("skills") or _extract_skills(f"{title} {description}"),
        "source_name": raw.get("source_name") or source_name,
        "source_url": raw.get("source_url") or raw.get("redirect_url") or "",
        "posted_at": raw.get("posted_at") or raw.get("posted_date") or raw.get("created"),
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "freshness_score": raw.get("freshness_score"),
    }


def normalize_postings(raw_postings: List[Dict[str, Any]], source_name: str = "sample") -> List[Dict[str, Any]]:
    normalized = []
    for raw in raw_postings:
        posting = normalize_posting(raw, source_name=source_name)
        if posting:
            normalized.append(posting)
    return normalized
