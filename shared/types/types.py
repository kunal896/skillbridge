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

@dataclass
class JobPosting:
    job_id: str
    title: str
    company: Optional[str]
    location: Optional[str]
    region: Optional[str]
    description: str
    skills: list[str] = field(default_factory=list)
    source_name: str = ""
    source_url: str = ""
    posted_at: Optional[str] = None
    fetched_at: Optional[str] = None
    freshness_score: Optional[float] = None

@dataclass
class LearnerProfile:
    learner_id: str
    current_role: Optional[str]
    target_role: str
    skills: list[SkillAssessment] = field(default_factory=list)
    experience_years: Optional[int] = None
    education: Optional[str] = None
    preferred_region: Optional[str] = None
    preferred_language: Optional[str] = None
    source: str = "manual"
    verified_skills: list[str] = field(default_factory=list)
