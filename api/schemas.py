"""
Pydantic schemas for API request/response validation.

Defines all input/output models for the REST API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================
# Resume Schemas
# ============================================================


class ContactInfoSchema(BaseModel):
    """Contact information schema."""

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None


class WorkExperienceSchema(BaseModel):
    """Work experience entry schema."""

    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    is_current: bool = False


class EducationSchema(BaseModel):
    """Education entry schema."""

    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None


class ResumeDataSchema(BaseModel):
    """Resume data schema matching Resume dataclass."""

    raw_text: str = ""
    contact: Optional[ContactInfoSchema] = None
    skills: List[str] = Field(default_factory=list)
    experience: List[WorkExperienceSchema] = Field(default_factory=list)
    education: List[EducationSchema] = Field(default_factory=list)
    sections: Dict[str, Any] = Field(default_factory=dict)
    file_path: Optional[str] = None
    file_type: Optional[str] = None


class ResumeUploadRequest(BaseModel):
    """Request to upload a parsed resume."""

    resume_json: Dict[str, Any] = Field(
        ..., description="Parsed resume data from resume_parser"
    )


class ResumeUploadResponse(BaseModel):
    """Response after uploading a resume."""

    resume_id: str
    message: str
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    skills_count: int


class ResumeGetResponse(BaseModel):
    """Response for getting a resume."""

    resume_id: str
    resume_data: Dict[str, Any]
    created_at: Optional[datetime] = None


# ============================================================
# Job Schemas
# ============================================================


class JobCreateRequest(BaseModel):
    """Request to create a job posting."""

    title: str = Field(..., min_length=1, description="Job title")
    company: str = Field(..., min_length=1, description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    raw_text: str = Field(
        ..., min_length=10, description="Full job description text"
    )
    required_skills: Optional[List[str]] = Field(
        None, description="Override extracted required skills"
    )
    preferred_skills: Optional[List[str]] = Field(
        None, description="Override extracted preferred skills"
    )


class JobCreateResponse(BaseModel):
    """Response after creating a job."""

    job_id: str
    message: str
    title: str
    company: str
    required_skills_count: int
    preferred_skills_count: int


class JobGetResponse(BaseModel):
    """Response for getting a job."""

    job_id: str
    title: str
    company: str
    location: Optional[str]
    job_data: Dict[str, Any]
    created_at: Optional[datetime] = None
    is_active: bool


class JobListItem(BaseModel):
    """Single job in list response."""

    job_id: str
    title: str
    company: str
    location: Optional[str]


class JobListResponse(BaseModel):
    """Response for listing jobs."""

    count: int
    jobs: List[JobListItem]


# ============================================================
# Match Schemas
# ============================================================


class MatchRequest(BaseModel):
    """Request to calculate match between resume and job."""

    resume_id: str = Field(..., description="Resume ID")
    job_id: str = Field(..., description="Job ID")


class ExplainabilitySchema(BaseModel):
    """Match explainability data."""

    matched_skills: List[str] = Field(default_factory=list)
    missing_required_skills: List[str] = Field(default_factory=list)
    missing_preferred_skills: List[str] = Field(default_factory=list)
    skill_match_percentage: float = 0.0
    semantic_similarity: float = 0.0
    experience_match: Optional[str] = None
    education_match: Optional[str] = None
    explanation_text: Optional[str] = None


class MatchResponse(BaseModel):
    """Match result response."""

    match_id: Optional[str] = None
    resume_id: str
    job_id: str
    final_score: float = Field(..., ge=0, le=1, description="Final weighted score")
    semantic_score: float = Field(..., ge=0, le=1, description="Semantic similarity")
    skill_score: float = Field(..., ge=0, le=1, description="Skill match score")
    match_tier: str = Field(..., description="Quality tier: Excellent/Strong/Good/Fair/Weak")
    explainability: ExplainabilitySchema


class TopMatchesRequest(BaseModel):
    """Request for top matches."""

    job_id: str = Field(..., description="Job ID to get matches for")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")


class TopMatchesResponse(BaseModel):
    """Top matches response."""

    job_id: str
    total_matches: int
    matches: List[MatchResponse]


class ResumeMatchesRequest(BaseModel):
    """Request for jobs matching a resume."""

    resume_id: str = Field(..., description="Resume ID")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")


class ResumeMatchesResponse(BaseModel):
    """Jobs matching a resume response."""

    resume_id: str
    total_matches: int
    matches: List[MatchResponse]


# ============================================================
# Batch Processing Schemas
# ============================================================


class BatchMatchRequest(BaseModel):
    """Request for batch matching."""

    resume_id: str = Field(..., description="Resume to match")
    job_ids: List[str] = Field(..., description="Jobs to match against")


class BatchMatchResponse(BaseModel):
    """Batch match response."""

    resume_id: str
    matches: List[MatchResponse]


# ============================================================
# Health & Status Schemas
# ============================================================


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    database_connected: bool = False
    embedding_model_loaded: bool = False


class StatsResponse(BaseModel):
    """System statistics response."""

    total_resumes: int
    total_jobs: int
    total_matches: int
    active_jobs: int
