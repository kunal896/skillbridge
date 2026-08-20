from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ProfileSource(str, Enum):
    RESUME = "resume"
    MCQ = "mcq"
    MANUAL = "manual"


class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class RoadmapStepStatus(str, Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"


class VerificationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"


@dataclass
class SkillAssessment:
    name: str
    level: SkillLevel
    evidence: list[str] = field(default_factory=list)


@dataclass
class SkillGap:
    name: str
    priority: int
    reason: str
    evidence_job_ids: list[str] = field(default_factory=list)


@dataclass
class SkillRequirement:
    skill: str
    required_level: SkillLevel = SkillLevel.BEGINNER
    weight: float = 1.0


@dataclass
class SourceCitation:
    source_id: str
    title: str
    url: str
    source_name: str
    snippet: Optional[str] = None


@dataclass
class RoadmapStep:
    step_id: str
    skill: str
    title: str
    description: str
    reason: str
    status: RoadmapStepStatus
    citations: list[SourceCitation] = field(default_factory=list)


@dataclass
class TestCase:
    input_data: str
    expected_output: str


@dataclass
class RubricCriterion:
    name: str
    description: str
    max_score: float


@dataclass
class ApiError:
    code: str
    message: str

@dataclass
class MatchResult:
    employer_id: str
    learner_id: str
    role_title: str
    match_score: float
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    verified_skills: list[str] = field(default_factory=list)
    explanation: str = ""