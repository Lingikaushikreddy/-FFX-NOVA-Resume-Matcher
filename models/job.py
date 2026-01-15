"""
Job description data model.

Parallel structure to Resume model for consistent handling.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
import json


@dataclass
class JobRequirement:
    """
    A single job requirement or qualification.

    Attributes:
        requirement_type: 'required' or 'preferred'.
        description: Text description of the requirement.
        category: Category like 'education', 'experience', 'skill'.
    """

    requirement_type: str = "required"
    description: str = ""
    category: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class Job:
    """
    Complete job description data structure.

    Attributes:
        raw_text: Original job description text.
        title: Job title/position name.
        company: Company name.
        location: Job location (city, remote, etc.).
        required_skills: Skills that are mandatory.
        preferred_skills: Skills that are nice-to-have.
        min_experience_years: Minimum years of experience required.
        education_requirements: Required education levels.
        responsibilities: List of job responsibilities.
        benefits: List of job benefits.
        job_id: Unique identifier (set when stored).
        created_at: Timestamp when created.
    """

    raw_text: str = ""
    title: str = ""
    company: str = ""
    location: Optional[str] = None
    is_remote: bool = False
    required_skills: list[str] = field(default_factory=list)
    preferred_skills: list[str] = field(default_factory=list)
    min_experience_years: Optional[int] = None
    max_experience_years: Optional[int] = None
    education_requirements: list[str] = field(default_factory=list)
    responsibilities: list[str] = field(default_factory=list)
    benefits: list[str] = field(default_factory=list)
    salary_range: Optional[str] = None
    job_id: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def get_all_skills(self) -> list[str]:
        """
        Get combined list of all skills.

        Returns:
            List of unique skills (required + preferred).
        """
        return list(set(self.required_skills + self.preferred_skills))

    def get_summary(self) -> dict:
        """
        Get a brief summary of the job.

        Returns:
            Dictionary with key job information.
        """
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "required_skills_count": len(self.required_skills),
            "preferred_skills_count": len(self.preferred_skills),
            "min_experience": self.min_experience_years,
        }
