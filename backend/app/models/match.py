import uuid
from datetime import datetime
from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class MatchResult(Base):
    __tablename__ = "match_results"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    learner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    role_title: Mapped[str] = mapped_column(String(160), nullable=False)
    match_score: Mapped[float] = mapped_column(Float, nullable=False)
    matched_skills_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    missing_skills_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    verified_skills_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
