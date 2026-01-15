"""
Job description parser.

Parses job descriptions into structured Job objects,
extracting skills, requirements, and other information.
"""

from typing import Optional
import re
import logging

from models.job import Job
from job_parser.extractors.skill_extractor import JobSkillExtractor
from job_parser.extractors.requirement_extractor import RequirementExtractor

logger = logging.getLogger(__name__)


class JobParser:
    """
    Parse job descriptions into structured Job objects.

    Mirrors the architecture of ResumeParser for consistency.

    Example:
        parser = JobParser()
        job = parser.parse_text(job_description, title="Python Developer")
    """

    def __init__(self, custom_skills: Optional[list[str]] = None):
        """
        Initialize the job parser.

        Args:
            custom_skills: Additional custom skills to recognize.
        """
        self.custom_skills = custom_skills or []
        self._skill_extractor = JobSkillExtractor(custom_skills=custom_skills)
        self._requirement_extractor = RequirementExtractor()

    def parse_text(
        self,
        text: str,
        title: str = "",
        company: str = "",
        location: Optional[str] = None,
    ) -> Job:
        """
        Parse job description text into a Job object.

        Args:
            text: Job description text.
            title: Job title (extracted from text if not provided).
            company: Company name.
            location: Job location.

        Returns:
            Parsed Job object.
        """
        job = Job(
            raw_text=text,
            title=title,
            company=company,
            location=location,
        )

        # Extract skills with priority
        skill_results = self._skill_extractor.extract_with_priority(text)
        job.required_skills = skill_results.get("required", [])
        job.preferred_skills = skill_results.get("preferred", [])

        # Extract requirements
        requirements = self._requirement_extractor.extract(text)
        job.education_requirements = [
            r.description for r in requirements if r.category == "education"
        ]

        # Extract experience years
        experience = self._requirement_extractor.extract_experience_years(text)
        if experience:
            job.min_experience_years = experience[0]
            job.max_experience_years = experience[1]

        # Extract location info
        location_info = self._requirement_extractor.extract_location_requirements(text)
        job.is_remote = location_info.get("is_remote", False)

        # Extract title if not provided
        if not job.title:
            job.title = self._extract_title(text)

        # Extract responsibilities
        job.responsibilities = self._extract_responsibilities(text)

        # Extract benefits
        job.benefits = self._extract_benefits(text)

        return job

    def _extract_title(self, text: str) -> str:
        """
        Extract job title from text.

        Args:
            text: Job description text.

        Returns:
            Extracted title or default.
        """
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if lines:
            # First non-empty line is often the title
            first_line = lines[0]
            # Clean it up
            if len(first_line) <= 100:
                return first_line

        return "Unknown Position"

    def _extract_responsibilities(self, text: str) -> list[str]:
        """
        Extract job responsibilities.

        Args:
            text: Job description text.

        Returns:
            List of responsibility strings.
        """
        responsibilities = []

        # Find responsibilities section
        section = self._find_section(
            text,
            [
                "responsibilities",
                "what you'll do",
                "what you will do",
                "your role",
                "job duties",
                "key responsibilities",
            ],
        )

        if section:
            # Extract bullet points
            lines = section.split("\n")
            for line in lines:
                line = line.strip()
                # Remove common bullet characters
                line = re.sub(r"^[\s•●○▪\-\*\+]+\s*", "", line)
                if line and len(line) > 10:
                    responsibilities.append(line)

        return responsibilities[:10]  # Limit to 10

    def _extract_benefits(self, text: str) -> list[str]:
        """
        Extract job benefits.

        Args:
            text: Job description text.

        Returns:
            List of benefit strings.
        """
        benefits = []

        # Find benefits section
        section = self._find_section(
            text,
            [
                "benefits",
                "perks",
                "what we offer",
                "we offer",
                "compensation",
                "why join us",
            ],
        )

        if section:
            lines = section.split("\n")
            for line in lines:
                line = line.strip()
                line = re.sub(r"^[\s•●○▪\-\*\+]+\s*", "", line)
                if line and len(line) > 5:
                    benefits.append(line)

        return benefits[:10]  # Limit to 10

    def _find_section(self, text: str, keywords: list[str]) -> str:
        """
        Find section containing any of the keywords.

        Args:
            text: Full text to search.
            keywords: Keywords indicating section start.

        Returns:
            Section content or empty string.
        """
        lines = text.split("\n")
        section_start = -1

        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(kw in line_lower for kw in keywords):
                section_start = i
                break

        if section_start == -1:
            return ""

        # Find next section
        section_end = len(lines)
        for i in range(section_start + 1, len(lines)):
            if self._is_section_header(lines[i]):
                section_end = i
                break

        return "\n".join(lines[section_start:section_end])

    def _is_section_header(self, line: str) -> bool:
        """Check if line is a section header."""
        line = line.strip()
        if not line:
            return False
        if len(line) > 50:
            return False
        if line.isupper():
            return True
        if line.endswith(":"):
            return True
        return False


def parse_job_text(
    text: str,
    title: str = "",
    company: str = "",
    location: Optional[str] = None,
) -> Job:
    """
    Convenience function to parse job text.

    Args:
        text: Job description text.
        title: Job title.
        company: Company name.
        location: Job location.

    Returns:
        Parsed Job object.
    """
    parser = JobParser()
    return parser.parse_text(text, title, company, location)
