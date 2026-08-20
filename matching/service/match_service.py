from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from shared.types.types import MatchResult
from matching.model.matcher import LearnerSkillInput, SkillMatchModel, SkillRequirementInput


@dataclass(frozen=True)
class LearnerForMatching:
    learner_id: str | UUID
    target_role: str
    skills: list[LearnerSkillInput]
    verified_skills: list[str]


@dataclass(frozen=True)
class EmployerForMatching:
    employer_id: str | UUID
    role_title: str
    required_skills: list[SkillRequirementInput]
    description: str | None = None


class MatchingService:
    """Public matching service used by the integration layer."""

    def __init__(self, model: SkillMatchModel | None = None) -> None:
        self.model = model or SkillMatchModel()

    def match(
        self,
        learner: LearnerForMatching,
        employer: EmployerForMatching,
    ) -> MatchResult:
        computation = self.model.compute(
            required_skills=employer.required_skills,
            learner_skills=learner.skills,
            verified_skills=learner.verified_skills,
        )
        return MatchResult(
            employer_id=str(employer.employer_id),
            learner_id=str(learner.learner_id),
            role_title=employer.role_title,
            match_score=computation.score,
            matched_skills=computation.matched_skills,
            missing_skills=computation.missing_skills,
            verified_skills=computation.verified_skills,
            explanation=computation.explanation,
        )

    def rank_learners(
        self,
        learners: list[LearnerForMatching],
        employer: EmployerForMatching,
        *,
        limit: int = 20,
    ) -> list[MatchResult]:
        results = [self.match(learner, employer) for learner in learners]
        results.sort(key=lambda result: result.match_score, reverse=True)
        return results[:limit]
