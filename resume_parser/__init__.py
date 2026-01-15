"""
Resume Parser Module for FFX NOVA Resume Matching Platform.

This module provides comprehensive resume parsing capabilities including:
- PDF and DOCX text extraction
- Section identification
- Skill, experience, education, and contact extraction
- Structured JSON output

Example usage:
    from resume_parser import ResumeParser

    parser = ResumeParser()
    result = parser.parse("resume.pdf")
    print(result.to_json())
"""

from resume_parser.parser import ResumeParser, parse_resume, parse_resume_text
from resume_parser.models.resume import (
    Resume,
    ContactInfo,
    WorkExperience,
    Education,
    ParsedSection,
)

__version__ = "1.0.0"
__author__ = "FFX NOVA Team"

__all__ = [
    "ResumeParser",
    "parse_resume",
    "parse_resume_text",
    "Resume",
    "ContactInfo",
    "WorkExperience",
    "Education",
    "ParsedSection",
]
