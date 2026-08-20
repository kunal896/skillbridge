from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from shared.types.types import SkillLevel
from matching.features.skill_features import normalize_skill, normalize_skill_set, SkillEvidence

LEVEL_WEIGHT = {
    SkillLevel.BEGINNER.value: 0.75,
    SkillLevel.INTERMEDIATE.value: 0.90,
    SkillLevel.ADVANCED.value: 1.00,
}


@dataclass(frozen=True)
class SkillRequirementInput:
    skill: str
    required_level: str = SkillLevel.BEGINNER.value
    weight: float = 1.0


@dataclass(frozen=True)
class LearnerSkillInput:
    skill: str
    level: str = SkillLevel.BEGINNER.value


@dataclass(frozen=True)
class MatchComputation:
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    verified_skills: list[str]
    evidence: list[SkillEvidence]
    explanation: str


class SkillMatchModel:
    """Deterministic, explainable MVP matching model.

    This deliberately uses verified skills as a first-class signal because the
    product's differentiator is that competence must be demonstrated, not only
    self-reported. The class is also intentionally isolated so it can later be
    replaced by a learned classifier without changing the service boundary.
    """

    def compute(
        self,
        required_skills: Iterable[SkillRequirementInput],
        learner_skills: Iterable[LearnerSkillInput],
        verified_skills: Iterable[str],
    ) -> MatchComputation:
        requirements = list(required_skills)
        learner_map = {
            normalize_skill(item.skill): item for item in learner_skills
        }
        verified = normalize_skill_set(list(verified_skills))

        total_weight = sum(max(0.0, req.weight) for req in requirements) or 1.0
        weighted_coverage = 0.0
        matched: list[str] = []
        missing: list[str] = []
        verified_names: list[str] = []
        evidence: list[SkillEvidence] = []

        for req in requirements:
            canonical = normalize_skill(req.skill)
            learner = learner_map.get(canonical)
            is_matched = learner is not None
            is_verified = canonical in verified
            level_factor = LEVEL_WEIGHT.get(
                getattr(learner, "level", SkillLevel.BEGINNER.value),
                LEVEL_WEIGHT[SkillLevel.BEGINNER.value],
            ) if learner else 0.0

            # A matched skill receives up to 60% of its contribution from
            # possession/level and an additional 40% when actually verified.
            contribution = 0.0
            if is_matched:
                contribution = 0.60 * level_factor
                matched.append(req.skill)
            else:
                missing.append(req.skill)

            if is_verified:
                contribution += 0.40
                verified_names.append(req.skill)

            weighted_coverage += max(0.0, req.weight) * contribution
            reason = "missing"
            if is_verified:
                reason = "verified"
            elif is_matched:
                reason = "present but not verified"

            evidence.append(
                SkillEvidence(
                    skill=req.skill,
                    required=True,
                    matched=is_matched,
                    verified=is_verified,
                    weight=req.weight,
                    reason=reason,
                )
            )

        score = max(0.0, min(1.0, weighted_coverage / total_weight))
        explanation = self._build_explanation(
            score=score,
            matched=matched,
            missing=missing,
            verified=verified_names,
        )

        return MatchComputation(
            score=score,
            matched_skills=matched,
            missing_skills=missing,
            verified_skills=verified_names,
            evidence=evidence,
            explanation=explanation,
        )

    @staticmethod
    def _build_explanation(
        *,
        score: float,
        matched: list[str],
        missing: list[str],
        verified: list[str],
    ) -> str:
        score_pct = round(score * 100)
        if verified:
            opening = f"{score_pct}% match with {len(verified)} verified skill(s)."
        else:
            opening = f"{score_pct}% match with no verified skills yet."

        matched_text = ", ".join(matched) if matched else "none"
        missing_text = ", ".join(missing) if missing else "none"
        verified_text = ", ".join(verified) if verified else "none"
        return (
            f"{opening} Matched: {matched_text}. "
            f"Verified: {verified_text}. Missing: {missing_text}."
        )
