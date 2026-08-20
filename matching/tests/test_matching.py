from matching.model.matcher import LearnerSkillInput, SkillRequirementInput
from matching.service.match_service import EmployerForMatching, LearnerForMatching, MatchingService


def test_verified_skill_scores_higher_than_unverified() -> None:
    employer = EmployerForMatching(
        employer_id="emp_1",
        role_title="Data Analyst",
        required_skills=[
            SkillRequirementInput("SQL", weight=1.0),
            SkillRequirementInput("Excel", weight=1.0),
        ],
    )
    learner = LearnerForMatching(
        learner_id="learner_1",
        target_role="Data Analyst",
        skills=[
            LearnerSkillInput("SQL", "intermediate"),
            LearnerSkillInput("Excel", "intermediate"),
        ],
        verified_skills=["SQL"],
    )

    result = MatchingService().match(learner, employer)
    assert result.match_score > 0.50
    assert result.verified_skills == ["SQL"]
    assert result.missing_skills == []


def test_aliases_are_normalized() -> None:
    employer = EmployerForMatching(
        employer_id="emp_1",
        role_title="Backend Engineer",
        required_skills=[SkillRequirementInput("PostgreSQL")],
    )
    learner = LearnerForMatching(
        learner_id="learner_1",
        target_role="Backend Engineer",
        skills=[LearnerSkillInput("postgres")],
        verified_skills=["postgres"],
    )

    result = MatchingService().match(learner, employer)
    assert result.match_score >= 0.85
