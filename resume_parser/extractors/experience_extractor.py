"""
Work experience extraction module.

This module extracts work experience entries from resume text,
including company names, job titles, dates, and descriptions.
"""

import re
from typing import Optional
import logging

from resume_parser.models.resume import WorkExperience
from resume_parser.utils.text_utils import (
    split_date_range,
    extract_lines,
    remove_bullets_and_numbering,
)

logger = logging.getLogger(__name__)


# Common job title patterns
JOB_TITLE_PATTERNS: list[str] = [
    # Executive/Senior titles
    r"(?:Chief|Senior|Lead|Principal|Staff)\s+\w+(?:\s+\w+)?(?:\s+Officer)?",
    r"(?:VP|Vice\s+President)\s+(?:of\s+)?\w+(?:\s+\w+)?",
    r"Director\s+(?:of\s+)?\w+(?:\s+\w+)?",
    # Standard titles
    r"(?:Software|Hardware|Systems?|Data|DevOps|Cloud|Full[\s-]?Stack|Front[\s-]?End|Back[\s-]?End)\s+(?:Engineer|Developer|Architect)",
    r"(?:Product|Program|Project|Engineering|Technical)\s+Manager",
    r"(?:Business|Data|Systems?|Financial|Operations)\s+Analyst",
    r"(?:UX|UI|Product|Graphic|Visual)\s+Designer",
    r"(?:QA|Quality\s+Assurance|Test)\s+(?:Engineer|Analyst|Lead)",
    r"(?:Machine\s+Learning|ML|AI|Data)\s+(?:Engineer|Scientist)",
    r"(?:Site\s+Reliability|SRE|Platform)\s+Engineer",
    r"(?:Technical|Solutions?)\s+(?:Architect|Consultant)",
    r"(?:Database|DBA|Systems?)\s+Administrator",
    r"(?:Security|Information\s+Security|Cybersecurity)\s+(?:Engineer|Analyst|Specialist)",
    r"(?:Network|Infrastructure)\s+Engineer",
    r"(?:IT|Information\s+Technology)\s+(?:Manager|Director|Specialist)",
    r"Scrum\s+Master",
    r"(?:Intern|Trainee|Apprentice)\s*(?:\w+)?",
    r"\w+\s+(?:Intern|Internship)",
    r"(?:Junior|Mid[\s-]?Level|Senior)\s+\w+(?:\s+\w+)?",
    # General patterns
    r"(?:Head|Manager|Lead|Supervisor)\s+(?:of\s+)?\w+(?:\s+\w+)?",
]

# Date patterns commonly found in experience sections
DATE_PATTERNS: list[str] = [
    # Month Year - Month Year or Present
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\s*[-–—]\s*(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|Present|Current|Now)",
    # MM/YYYY - MM/YYYY or Present
    r"\d{1,2}/\d{4}\s*[-–—]\s*(?:\d{1,2}/\d{4}|Present|Current|Now)",
    # YYYY - YYYY or Present
    r"\d{4}\s*[-–—]\s*(?:\d{4}|Present|Current|Now)",
    # Just YYYY (single year)
    r"\b\d{4}\b",
]


class ExperienceExtractor:
    """
    Extract work experience from resume text.

    Parses experience sections to identify individual positions,
    including company names, job titles, employment dates, and
    job descriptions.

    Example:
        extractor = ExperienceExtractor()
        experiences = extractor.extract(experience_section_text)
    """

    def __init__(self) -> None:
        """Initialize the experience extractor with compiled patterns."""
        self._job_title_patterns = [
            re.compile(p, re.IGNORECASE) for p in JOB_TITLE_PATTERNS
        ]
        self._date_patterns = [
            re.compile(p, re.IGNORECASE) for p in DATE_PATTERNS
        ]

    def extract(
        self,
        text: str,
        experience_section: Optional[str] = None,
    ) -> list[WorkExperience]:
        """
        Extract work experiences from resume text.

        Args:
            text: Full resume text.
            experience_section: Optional experience section content.

        Returns:
            List of WorkExperience objects.
        """
        # Prefer experience section if available
        search_text = experience_section if experience_section else text

        if not search_text:
            return []

        # Split into potential experience blocks
        blocks = self._split_into_experience_blocks(search_text)

        experiences: list[WorkExperience] = []
        for block in blocks:
            experience = self._parse_experience_block(block)
            if experience and (experience.company or experience.role):
                experiences.append(experience)

        return experiences

    def _split_into_experience_blocks(self, text: str) -> list[str]:
        """
        Split experience section into individual job blocks.

        Args:
            text: Experience section text.

        Returns:
            List of text blocks, each representing one job.
        """
        lines = text.split("\n")
        blocks: list[str] = []
        current_block: list[str] = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this line starts a new experience block
            # (contains a date range or looks like a header)
            is_new_block = False

            # Check for date patterns that indicate a new position
            for pattern in self._date_patterns:
                if pattern.search(line):
                    # If we have content and this looks like a new entry
                    if current_block and self._looks_like_header(line):
                        is_new_block = True
                    break

            if is_new_block and current_block:
                blocks.append("\n".join(current_block))
                current_block = []

            current_block.append(line)

        # Don't forget the last block
        if current_block:
            blocks.append("\n".join(current_block))

        return blocks

    def _looks_like_header(self, line: str) -> bool:
        """
        Check if a line looks like a job header.

        Args:
            line: Line to check.

        Returns:
            True if line appears to be a job header.
        """
        # Contains a date range
        for pattern in self._date_patterns:
            if pattern.search(line):
                return True

        # Matches a job title pattern
        for pattern in self._job_title_patterns:
            if pattern.search(line):
                return True

        return False

    def _parse_experience_block(self, block: str) -> Optional[WorkExperience]:
        """
        Parse a single experience block into WorkExperience.

        Args:
            block: Text block for one job.

        Returns:
            WorkExperience object, or None if parsing fails.
        """
        lines = extract_lines(block)
        if not lines:
            return None

        experience = WorkExperience()

        # Extract dates from anywhere in the block
        date_range = self._extract_date_range(block)
        if date_range:
            experience.start_date, experience.end_date = date_range
            experience.is_current = (
                experience.end_date
                and experience.end_date.lower() in ("present", "current", "now")
            )

        # First few lines typically contain title/company
        header_lines = lines[:3]

        # Try to identify role and company
        role, company = self._extract_role_and_company(header_lines, block)
        experience.role = role
        experience.company = company

        # Rest is description
        description_lines = lines[2:] if len(lines) > 2 else []
        if description_lines:
            description = "\n".join(description_lines)
            description = remove_bullets_and_numbering(description)
            experience.description = description.strip()

        # Try to extract location
        experience.location = self._extract_location(block)

        return experience

    def _extract_date_range(self, text: str) -> Optional[tuple[Optional[str], Optional[str]]]:
        """
        Extract date range from text.

        Args:
            text: Text containing dates.

        Returns:
            Tuple of (start_date, end_date), or None if not found.
        """
        for pattern in self._date_patterns:
            match = pattern.search(text)
            if match:
                date_str = match.group()
                return split_date_range(date_str)

        return None

    def _extract_role_and_company(
        self,
        header_lines: list[str],
        full_block: str,
    ) -> tuple[Optional[str], Optional[str]]:
        """
        Extract job role and company name from header lines.

        Args:
            header_lines: First few lines of the experience block.
            full_block: Complete block text for fallback.

        Returns:
            Tuple of (role, company).
        """
        role: Optional[str] = None
        company: Optional[str] = None

        # Look for job title patterns
        for line in header_lines:
            # Remove dates from line for cleaner matching
            clean_line = line
            for pattern in self._date_patterns:
                clean_line = pattern.sub("", clean_line).strip()

            # Check for job title
            if not role:
                for pattern in self._job_title_patterns:
                    match = pattern.search(clean_line)
                    if match:
                        role = match.group().strip()
                        # Remove the role from the line to help find company
                        clean_line = clean_line.replace(role, "").strip()
                        break

            # Whatever remains might be the company
            if clean_line and not company:
                # Clean up common separators
                clean_line = re.sub(r"^[\s,|•\-–—at@]+", "", clean_line)
                clean_line = re.sub(r"[\s,|•\-–—]+$", "", clean_line)
                if clean_line and len(clean_line) > 2:
                    company = clean_line

        # If we still don't have a role, use the first non-empty line
        if not role and header_lines:
            for line in header_lines:
                clean_line = line
                for pattern in self._date_patterns:
                    clean_line = pattern.sub("", clean_line).strip()
                if clean_line and len(clean_line) > 2:
                    role = clean_line
                    break

        return role, company

    def _extract_location(self, text: str) -> Optional[str]:
        """
        Extract work location from experience block.

        Args:
            text: Experience block text.

        Returns:
            Location string, or None.
        """
        # Common location patterns
        location_patterns = [
            r"(?:Remote|Hybrid|On-?site)",
            r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?,\s*[A-Z]{2}\b",  # City, ST
            r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s+[A-Z][a-z]+)?\b",  # City, State
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()

        return None
