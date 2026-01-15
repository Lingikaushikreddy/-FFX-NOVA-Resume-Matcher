"""
Data models for resume parsing.

This module defines Pydantic models for structured resume data including
contact information, work experience, education, and skills.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import date
import json


@dataclass
class ContactInfo:
    """
    Contact information extracted from a resume.

    Attributes:
        email: Primary email address.
        phone: Phone number in original format.
        location: City, state, or full address.
        linkedin: LinkedIn profile URL if found.
        name: Full name of the candidate.
    """

    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    name: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class WorkExperience:
    """
    A single work experience entry.

    Attributes:
        company: Name of the employer.
        role: Job title or position.
        start_date: Employment start date.
        end_date: Employment end date (None if current).
        description: Job description or responsibilities.
        location: Work location if specified.
        is_current: Whether this is the current position.
    """

    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_current: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class Education:
    """
    An educational qualification entry.

    Attributes:
        institution: Name of the educational institution.
        degree: Type of degree (e.g., Bachelor's, Master's).
        field_of_study: Major or field of study.
        graduation_date: Date of graduation or expected graduation.
        gpa: Grade point average if mentioned.
        honors: Any honors or distinctions.
    """

    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class ParsedSection:
    """
    A section identified in the resume.

    Attributes:
        name: Section name (e.g., 'Experience', 'Education').
        content: Raw text content of the section.
        start_index: Character position where section starts.
        end_index: Character position where section ends.
    """

    name: str
    content: str
    start_index: int = 0
    end_index: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class Resume:
    """
    Complete parsed resume data structure.

    This is the main output class containing all extracted resume information
    in a structured format.

    Attributes:
        raw_text: Original extracted text from the document.
        contact: Extracted contact information.
        skills: List of identified skills.
        experience: List of work experience entries.
        education: List of education entries.
        sections: Dictionary of identified sections.
        file_path: Original file path of the resume.
        file_type: File extension (pdf, docx, etc.).
        parse_errors: List of any errors encountered during parsing.
    """

    raw_text: str = ""
    contact: ContactInfo = field(default_factory=ContactInfo)
    skills: list[str] = field(default_factory=list)
    experience: list[WorkExperience] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    sections: dict[str, ParsedSection] = field(default_factory=dict)
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    parse_errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """
        Convert the resume to a dictionary representation.

        Returns:
            Dictionary containing all resume data.
        """
        return {
            "raw_text": self.raw_text,
            "contact": self.contact.to_dict(),
            "skills": self.skills,
            "experience": [exp.to_dict() for exp in self.experience],
            "education": [edu.to_dict() for edu in self.education],
            "sections": {name: sec.to_dict() for name, sec in self.sections.items()},
            "file_path": self.file_path,
            "file_type": self.file_type,
            "parse_errors": self.parse_errors,
        }

    def to_json(self, indent: int = 2) -> str:
        """
        Convert the resume to a JSON string.

        Args:
            indent: Number of spaces for JSON indentation.

        Returns:
            JSON string representation of the resume.
        """
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def get_summary(self) -> dict:
        """
        Get a brief summary of the parsed resume.

        Returns:
            Dictionary with counts and key information.
        """
        return {
            "name": self.contact.name,
            "email": self.contact.email,
            "skills_count": len(self.skills),
            "experience_count": len(self.experience),
            "education_count": len(self.education),
            "sections_found": list(self.sections.keys()),
            "has_errors": len(self.parse_errors) > 0,
        }
