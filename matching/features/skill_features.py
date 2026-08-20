from __future__ import annotations

import re
from dataclasses import dataclass

# Small, explicit alias table. This keeps the matcher stable and explainable.
SKILL_ALIASES: dict[str, set[str]] = {
    "python": {"python", "python 3", "python3"},
    "sql": {"sql", "structured query language", "mysql", "postgresql", "postgres"},
    "excel": {"excel", "microsoft excel", "ms excel", "spreadsheets", "spreadsheet"},
    "power bi": {"power bi", "powerbi", "microsoft power bi"},
    "tableau": {"tableau"},
    "pandas": {"pandas", "python pandas"},
    "numpy": {"numpy"},
    "machine learning": {"machine learning", "ml", "machine-learning"},
    "data analysis": {"data analysis", "data analytics", "analytics"},
    "data visualization": {"data visualization", "data viz", "visualization"},
    "statistics": {"statistics", "statistical analysis", "stats"},
    "javascript": {"javascript", "js"},
    "typescript": {"typescript", "ts"},
    "react": {"react", "reactjs", "react.js"},
    "next.js": {"next.js", "nextjs", "next js"},
    "fastapi": {"fastapi"},
    "sqlalchemy": {"sqlalchemy"},
    "postgresql": {"postgresql", "postgres"},
    "git": {"git", "github", "gitlab"},
    "docker": {"docker", "containerization", "containers"},
}


def normalize_skill(value: str) -> str:
    """Return a canonical, comparison-friendly skill name."""
    value = value.strip().lower()
    value = re.sub(r"\s+", " ", value)
    value = value.replace("–", "-").replace("—", "-")

    for canonical, aliases in SKILL_ALIASES.items():
        if value in aliases:
            return canonical
    return value


def normalize_skill_set(skills: list[str]) -> set[str]:
    return {normalize_skill(skill) for skill in skills if skill and skill.strip()}


def skill_matches(left: str, right: str) -> bool:
    """Compare skills through canonical names rather than raw strings."""
    return normalize_skill(left) == normalize_skill(right)


@dataclass(frozen=True)
class SkillEvidence:
    skill: str
    required: bool
    matched: bool
    verified: bool
    weight: float
    reason: str
