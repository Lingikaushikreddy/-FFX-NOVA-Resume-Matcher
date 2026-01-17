"""
Job model for FFX NOVA job matching.

Enhanced job model with security clearance support for
federal/military job matching in Northern Virginia.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import IntEnum
import json
import uuid


class ClearanceLevel(IntEnum):
    """
    US Government security clearance levels.

    Ordered by hierarchy - higher values indicate higher clearance.
    """

    NONE = 0
    PUBLIC_TRUST = 1
    SECRET = 2
    TOP_SECRET = 3
    TS_SCI = 4


@dataclass
class Job:
    """
    Job posting with full metadata for matching.

    Attributes:
        job_id: Unique identifier.
        title: Job title.
        company: Company name.
        description: Full job description text.
        clearance_level: Required security clearance.
        required_skills: Must-have skills.
        preferred_skills: Nice-to-have skills.
        min_experience_years: Minimum years of experience.
        location: Job location.
        salary_min: Minimum salary.
        salary_max: Maximum salary.
        is_remote: Whether remote work is allowed.
        department: Department or team.
        employment_type: Full-time, part-time, contract, etc.

    Example:
        >>> job = Job(
        ...     title="Senior Python Developer",
        ...     company="Federal Contractor Inc",
        ...     description="Looking for Python expert...",
        ...     clearance_level=ClearanceLevel.SECRET,
        ...     required_skills=["Python", "Django", "AWS"],
        ...     min_experience_years=5,
        ... )
    """

    title: str
    company: str
    description: str = ""
    job_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    clearance_level: ClearanceLevel = ClearanceLevel.NONE
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    min_experience_years: int = 0
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    is_remote: bool = False
    department: Optional[str] = None
    employment_type: str = "Full-time"

    def get_all_skills(self) -> List[str]:
        """Get all skills (required + preferred)."""
        all_skills = list(self.required_skills) + list(self.preferred_skills)
        return list(dict.fromkeys(all_skills))  # Preserve order, remove dupes

    def get_clearance_string(self) -> str:
        """Get human-readable clearance level."""
        names = {
            ClearanceLevel.NONE: "None Required",
            ClearanceLevel.PUBLIC_TRUST: "Public Trust",
            ClearanceLevel.SECRET: "Secret",
            ClearanceLevel.TOP_SECRET: "Top Secret",
            ClearanceLevel.TS_SCI: "TS/SCI",
        }
        return names.get(self.clearance_level, "Unknown")

    def get_salary_range_string(self) -> Optional[str]:
        """Get formatted salary range."""
        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,} - ${self.salary_max:,}"
        elif self.salary_min:
            return f"${self.salary_min:,}+"
        elif self.salary_max:
            return f"Up to ${self.salary_max:,}"
        return None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "clearance_level": self.clearance_level.name,
            "required_skills": self.required_skills,
            "preferred_skills": self.preferred_skills,
            "min_experience_years": self.min_experience_years,
            "location": self.location,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "is_remote": self.is_remote,
            "department": self.department,
            "employment_type": self.employment_type,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "Job":
        """Create Job from dictionary."""
        clearance = data.get("clearance_level", "NONE")
        if isinstance(clearance, str):
            clearance = ClearanceLevel[clearance.upper()]

        return cls(
            job_id=data.get("job_id", str(uuid.uuid4())[:8]),
            title=data.get("title", ""),
            company=data.get("company", ""),
            description=data.get("description", ""),
            clearance_level=clearance,
            required_skills=data.get("required_skills", []),
            preferred_skills=data.get("preferred_skills", []),
            min_experience_years=data.get("min_experience_years", 0),
            location=data.get("location"),
            salary_min=data.get("salary_min"),
            salary_max=data.get("salary_max"),
            is_remote=data.get("is_remote", False),
            department=data.get("department"),
            employment_type=data.get("employment_type", "Full-time"),
        )

    def get_summary(self) -> dict:
        """Get job summary for display."""
        return {
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "location": self.location or "Not specified",
            "clearance": self.get_clearance_string(),
            "experience": f"{self.min_experience_years}+ years",
            "required_skills_count": len(self.required_skills),
            "preferred_skills_count": len(self.preferred_skills),
            "salary_range": self.get_salary_range_string(),
            "remote": "Yes" if self.is_remote else "No",
        }

    def __str__(self) -> str:
        """String representation."""
        return f"{self.title} @ {self.company}"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Job(title='{self.title}', company='{self.company}', "
            f"clearance={self.clearance_level.name}, "
            f"required_skills={len(self.required_skills)})"
        )
