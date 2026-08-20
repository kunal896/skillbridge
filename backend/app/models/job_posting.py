import uuid
from datetime import datetime
from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class JobPosting(Base):
    __tablename__ = "job_postings"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_job_id: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    company: Mapped[str|None] = mapped_column(String(200))
    location: Mapped[str|None] = mapped_column(String(200))
    region: Mapped[str|None] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source_name: Mapped[str] = mapped_column(String(80), nullable=False)
    source_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    posted_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True))
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    freshness_score: Mapped[float|None] = mapped_column(Float)
