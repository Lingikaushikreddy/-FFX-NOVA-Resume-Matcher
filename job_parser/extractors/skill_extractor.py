"""
Skill extraction for job descriptions.

Distinguishes between required and preferred skills
by analyzing context and section headers.
"""

import re
from typing import Optional
import logging

# Import the existing skill taxonomy from resume_parser
from resume_parser.extractors.skill_extractor import (
    SkillExtractor,
    TECHNICAL_SKILLS,
    SOFT_SKILLS,
)

logger = logging.getLogger(__name__)


class JobSkillExtractor:
    """
    Extract skills from job descriptions with priority levels.

    Identifies required vs preferred skills based on section
    context and keyword analysis.

    Example:
        extractor = JobSkillExtractor()
        result = extractor.extract_with_priority(job_text)
        # {"required": ["Python", "SQL"], "preferred": ["Docker"]}
    """

    # Keywords indicating required skills
    REQUIRED_KEYWORDS = [
        "required",
        "requirements",
        "must have",
        "must-have",
        "qualifications",
        "mandatory",
        "essential",
        "minimum requirements",
        "you will need",
        "you must have",
        "what you need",
    ]

    # Keywords indicating preferred skills
    PREFERRED_KEYWORDS = [
        "preferred",
        "nice to have",
        "nice-to-have",
        "bonus",
        "plus",
        "a plus",
        "desired",
        "additional",
        "good to have",
        "ideally",
        "advantageous",
    ]

    def __init__(self, custom_skills: Optional[list[str]] = None):
        """
        Initialize the job skill extractor.

        Args:
            custom_skills: Additional custom skills to recognize.
        """
        self._base_extractor = SkillExtractor(
            include_soft_skills=True,
            custom_skills=custom_skills or [],
        )

    def extract_with_priority(self, text: str) -> dict[str, list[str]]:
        """
        Extract skills and categorize as required or preferred.

        Args:
            text: Job description text.

        Returns:
            Dictionary with 'required' and 'preferred' skill lists.
        """
        if not text:
            return {"required": [], "preferred": []}

        # Find required and preferred sections
        required_section = self._find_section(text, self.REQUIRED_KEYWORDS)
        preferred_section = self._find_section(text, self.PREFERRED_KEYWORDS)

        # Extract from each section
        required_skills: set[str] = set()
        preferred_skills: set[str] = set()

        if required_section:
            required_skills = set(self._base_extractor.extract(required_section))

        if preferred_section:
            preferred_skills = set(self._base_extractor.extract(preferred_section))

        # If no clear sections found, extract from full text as required
        if not required_skills and not preferred_skills:
            all_skills = self._base_extractor.extract(text)
            required_skills = set(all_skills)

        # Remove duplicates (required takes precedence)
        preferred_skills = preferred_skills - required_skills

        return {
            "required": sorted(list(required_skills)),
            "preferred": sorted(list(preferred_skills)),
        }

    def extract_all(self, text: str) -> list[str]:
        """
        Extract all skills without priority distinction.

        Args:
            text: Job description text.

        Returns:
            List of all skills found.
        """
        return self._base_extractor.extract(text)

    def extract_by_category(self, text: str) -> dict[str, list[str]]:
        """
        Extract skills organized by category.

        Args:
            text: Job description text.

        Returns:
            Dictionary mapping category names to skill lists.
        """
        return self._base_extractor.extract_by_category(text)

    def _find_section(self, text: str, keywords: list[str]) -> str:
        """
        Find section containing any of the keywords.

        Args:
            text: Full text to search.
            keywords: Keywords indicating section start.

        Returns:
            Section content or empty string if not found.
        """
        lines = text.split("\n")
        section_start = -1

        # Find line containing any keyword
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(kw in line_lower for kw in keywords):
                section_start = i
                break

        if section_start == -1:
            return ""

        # Find next major section header
        section_end = len(lines)
        for i in range(section_start + 1, len(lines)):
            if self._is_section_header(lines[i]):
                section_end = i
                break

        return "\n".join(lines[section_start:section_end])

    def _is_section_header(self, line: str) -> bool:
        """
        Check if line is a section header.

        Args:
            line: Line of text.

        Returns:
            True if line appears to be a section header.
        """
        line = line.strip()
        if not line:
            return False

        # All uppercase or ends with colon
        if line.isupper() and len(line) < 50:
            return True
        if line.endswith(":") and len(line) < 50:
            return True

        # Common section header patterns
        section_patterns = [
            r"^(?:about|what|who|why|how)",
            r"^(?:requirements?|qualifications?|skills?)",
            r"^(?:responsibilities?|duties)",
            r"^(?:benefits?|perks?|compensation)",
            r"^(?:about\s+(?:us|the\s+(?:company|role|team)))",
        ]

        for pattern in section_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return True

        return False


def extract_job_skills(text: str) -> dict[str, list[str]]:
    """
    Convenience function to extract job skills.

    Args:
        text: Job description text.

    Returns:
        Dictionary with required and preferred skills.
    """
    extractor = JobSkillExtractor()
    return extractor.extract_with_priority(text)
