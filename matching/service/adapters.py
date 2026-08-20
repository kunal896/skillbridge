from __future__ import annotations

from typing import Any

from matching.model.matcher import LearnerSkillInput, SkillRequirementInput
from matching.service.match_service import EmployerForMatching, LearnerForMatching


def learner_from_contract(data: dict[str, Any]) -> LearnerForMatching:
    """Adapt shared LearnerProfile-style JSON into the matching domain."""
    skills: list[LearnerSkillInput] = []
    for item in data.get("skills", []):
        if isinstance(item, str):
            skills.append(LearnerSkillInput(skill=item))
        else:
            skills.append(
                LearnerSkillInput(
                    skill=item.get("name", ""),
                    level=item.get("level", "beginner"),
                )
            )

    return LearnerForMatching(
        learner_id=data["learner_id"],
        target_role=data["target_role"],
        skills=skills,
        # Verified skills are intentionally separate from self-reported skills.
        verified_skills=data.get("verified_skills", []),
    )


def employer_from_contract(data: dict[str, Any]) -> EmployerForMatching:
    requirements: list[SkillRequirementInput] = []
    for item in data.get("required_skills", []):
        if isinstance(item, str):
            requirements.append(SkillRequirementInput(skill=item))
        else:
            requirements.append(
                SkillRequirementInput(
                    skill=item.get("skill", ""),
                    required_level=item.get("required_level", "beginner"),
                    weight=float(item.get("weight", 1.0)),
                )
            )

    return EmployerForMatching(
        employer_id=data["employer_id"],
        role_title=data["role_title"],
        required_skills=requirements,
        description=data.get("description"),
    )


def match_result_to_backend_payload(result: Any) -> dict[str, Any]:
    """Convert shared MatchResult to the existing FastAPI /matches payload."""
    return {
        "employer_id": result.employer_id,
        "learner_id": result.learner_id,
        "role_title": result.role_title,
        "match_score": result.match_score,
        "matched_skills": result.matched_skills,
        "missing_skills": result.missing_skills,
        "verified_skills": result.verified_skills,
        "explanation": result.explanation,
    }
