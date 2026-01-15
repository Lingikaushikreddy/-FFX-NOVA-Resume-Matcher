"""
SQLAlchemy ORM models for PostgreSQL with pgvector.

Defines database tables for resumes, jobs, and match results
with vector embedding support for similarity search.
"""

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

# Conditional import for pgvector
try:
    from pgvector.sqlalchemy import Vector

    PGVECTOR_AVAILABLE = True
except ImportError:
    PGVECTOR_AVAILABLE = False
    Vector = None

Base = declarative_base()


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


class ResumeDB(Base):
    """
    Resume storage with embedding vector.

    Stores parsed resume data along with vector embedding
    for semantic similarity search.
    """

    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    # Resume data (stored as JSON)
    resume_json = Column(JSONB, nullable=False)
    raw_text = Column(Text, nullable=False)

    # Extracted fields for quick access
    candidate_name = Column(String(255))
    candidate_email = Column(String(255), index=True)
    skills = Column(JSONB)  # list[str]

    # Vector embedding (384 dimensions for all-MiniLM-L6-v2)
    # Note: Requires pgvector extension
    embedding = Column(Vector(384) if PGVECTOR_AVAILABLE else Text, nullable=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    file_path = Column(String(500))

    def __repr__(self) -> str:
        return f"<ResumeDB(id={self.id}, name={self.candidate_name})>"


class JobDB(Base):
    """
    Job posting storage with embedding vector.

    Stores job description data along with vector embedding
    for semantic matching with resumes.
    """

    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    # Job data (stored as JSON)
    job_json = Column(JSONB, nullable=False)
    raw_text = Column(Text, nullable=False)

    # Extracted fields for quick access
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), index=True)
    location = Column(String(255))
    required_skills = Column(JSONB)  # list[str]
    preferred_skills = Column(JSONB)  # list[str]

    # Vector embedding
    embedding = Column(Vector(384) if PGVECTOR_AVAILABLE else Text, nullable=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<JobDB(id={self.id}, title={self.title})>"


class MatchResultDB(Base):
    """
    Stored matching results.

    Caches match calculations between resumes and jobs
    for quick retrieval and ranking.
    """

    __tablename__ = "match_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    resume_id = Column(
        String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False
    )
    job_id = Column(
        String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )

    # Scores
    final_score = Column(Float, nullable=False, index=True)
    semantic_score = Column(Float, nullable=False)
    skill_score = Column(Float, nullable=False)

    # Explainability (stored as JSON)
    explainability_json = Column(JSONB, nullable=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Composite index for efficient job-based queries
    __table_args__ = (
        Index("ix_match_job_score", "job_id", "final_score"),
        Index("ix_match_resume", "resume_id"),
    )

    def __repr__(self) -> str:
        return f"<MatchResultDB(resume={self.resume_id}, job={self.job_id}, score={self.final_score})>"


# Create indexes for vector similarity search (requires pgvector)
# These will be created when init_db() is called
VECTOR_INDEXES = """
-- Create IVFFlat index for fast similarity search on resumes
CREATE INDEX IF NOT EXISTS ix_resumes_embedding
ON resumes USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create IVFFlat index for fast similarity search on jobs
CREATE INDEX IF NOT EXISTS ix_jobs_embedding
ON jobs USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
"""
