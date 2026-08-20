import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, Text, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from sqlalchemy import DateTime, Integer, String, Text, func
class Learner(Base):
    __tablename__ = "learners"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
        nullable=False,
    )

    current_role: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    target_role: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    preferred_region: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    preferred_language: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True,
    )

    resume_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    profile_source: Mapped[str] = mapped_column(
        String(20),
        default="manual",
        nullable=False,
    )

    experience_years: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    education: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    skills_json: Mapped[str] = mapped_column(
        Text,
        default="[]",
        nullable=False,
    )

    verified_skills_json: Mapped[str] = mapped_column(
        Text,
        default="[]",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )