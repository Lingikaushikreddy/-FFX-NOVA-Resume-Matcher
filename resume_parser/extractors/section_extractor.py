"""
Resume section identification module.

This module identifies and extracts distinct sections from resume text
such as Experience, Education, Skills, and Contact information.
"""

import re
from typing import Optional
import logging

from resume_parser.models.resume import ParsedSection
from resume_parser.utils.text_utils import is_likely_header

logger = logging.getLogger(__name__)


# Common section header patterns for resumes
SECTION_PATTERNS: dict[str, list[str]] = {
    "contact": [
        r"contact\s*(info|information|details)?",
        r"personal\s*(info|information|details)?",
        r"about\s*me",
    ],
    "summary": [
        r"(professional\s+)?(summary|profile|objective)",
        r"career\s*(summary|objective|profile)",
        r"executive\s+summary",
        r"overview",
    ],
    "experience": [
        r"(work|professional|employment)\s*(experience|history)",
        r"experience",
        r"work\s+history",
        r"career\s+history",
        r"professional\s+background",
    ],
    "education": [
        r"education(al)?\s*(background|history|qualifications)?",
        r"academic\s*(background|history|qualifications)?",
        r"degrees?\s*(&|and)?\s*certifications?",
    ],
    "skills": [
        r"(technical\s+)?skills?(\s*(&|and)\s*abilities)?",
        r"core\s+competencies",
        r"competencies",
        r"technical\s+(proficiencies|expertise)",
        r"areas?\s+of\s+expertise",
        r"proficiencies",
    ],
    "certifications": [
        r"certifications?\s*(&|and)?\s*(licenses?)?",
        r"licenses?\s*(&|and)?\s*certifications?",
        r"professional\s+certifications?",
        r"credentials",
    ],
    "projects": [
        r"(key\s+)?projects?",
        r"personal\s+projects?",
        r"professional\s+projects?",
        r"portfolio",
    ],
    "publications": [
        r"publications?",
        r"papers?",
        r"research\s*(papers?|publications?)?",
    ],
    "awards": [
        r"awards?\s*(&|and)?\s*(honors?|achievements?)?",
        r"honors?\s*(&|and)?\s*awards?",
        r"achievements?",
        r"recognition",
    ],
    "languages": [
        r"languages?",
        r"language\s+(proficiency|skills?)",
    ],
    "interests": [
        r"(personal\s+)?interests?",
        r"hobbies(\s*(&|and)\s*interests?)?",
        r"activities",
    ],
    "references": [
        r"references?",
        r"professional\s+references?",
    ],
    "volunteer": [
        r"volunteer\s*(experience|work)?",
        r"community\s+(service|involvement)",
    ],
}


class SectionExtractor:
    """
    Identify and extract sections from resume text.

    Uses pattern matching to identify common resume sections
    and extract their content.

    Example:
        extractor = SectionExtractor()
        sections = extractor.extract("... resume text ...")
    """

    def __init__(self, custom_patterns: Optional[dict[str, list[str]]] = None) -> None:
        """
        Initialize the section extractor.

        Args:
            custom_patterns: Additional section patterns to use.
        """
        self.patterns = SECTION_PATTERNS.copy()
        if custom_patterns:
            for section, patterns in custom_patterns.items():
                if section in self.patterns:
                    self.patterns[section].extend(patterns)
                else:
                    self.patterns[section] = patterns

        # Compile all patterns for efficiency
        self._compiled_patterns: dict[str, list[re.Pattern]] = {}
        for section, patterns in self.patterns.items():
            self._compiled_patterns[section] = [
                re.compile(rf"^\s*{p}\s*:?\s*$", re.IGNORECASE)
                for p in patterns
            ]

    def extract(self, text: str) -> dict[str, ParsedSection]:
        """
        Extract sections from resume text.

        Args:
            text: Full resume text content.

        Returns:
            Dictionary mapping section names to ParsedSection objects.
        """
        if not text:
            return {}

        lines = text.split("\n")
        section_markers: list[tuple[int, int, str]] = []  # (line_idx, char_idx, section_name)

        current_char_idx = 0
        for line_idx, line in enumerate(lines):
            section_name = self._identify_section(line)
            if section_name:
                section_markers.append((line_idx, current_char_idx, section_name))
            current_char_idx += len(line) + 1  # +1 for newline

        if not section_markers:
            # Try to infer sections from content structure
            return self._infer_sections(text)

        # Extract content between sections
        sections: dict[str, ParsedSection] = {}

        for i, (line_idx, start_char, section_name) in enumerate(section_markers):
            # Calculate end position
            if i + 1 < len(section_markers):
                end_line_idx = section_markers[i + 1][0]
                end_char = section_markers[i + 1][1]
            else:
                end_line_idx = len(lines)
                end_char = len(text)

            # Extract section content (excluding the header line)
            section_lines = lines[line_idx + 1:end_line_idx]
            content = "\n".join(section_lines).strip()

            if content:
                sections[section_name] = ParsedSection(
                    name=section_name,
                    content=content,
                    start_index=start_char,
                    end_index=end_char,
                )

        return sections

    def _identify_section(self, line: str) -> Optional[str]:
        """
        Identify if a line is a section header.

        Args:
            line: Line of text to check.

        Returns:
            Section name if identified, None otherwise.
        """
        line = line.strip()

        if not line or not is_likely_header(line):
            return None

        # Remove common punctuation for matching
        clean_line = re.sub(r"[:\-–—]$", "", line).strip()

        for section_name, patterns in self._compiled_patterns.items():
            for pattern in patterns:
                if pattern.match(clean_line):
                    return section_name

        return None

    def _infer_sections(self, text: str) -> dict[str, ParsedSection]:
        """
        Attempt to infer sections when explicit headers aren't found.

        Uses content analysis to identify likely section boundaries.

        Args:
            text: Resume text content.

        Returns:
            Dictionary of inferred sections.
        """
        sections: dict[str, ParsedSection] = {}

        # Look for patterns that indicate specific content
        # This is a fallback when explicit headers aren't present

        # Check for experience-like patterns (company names, dates)
        experience_pattern = r"(?:\d{4}\s*[-–]\s*(?:\d{4}|present|current))"
        if re.search(experience_pattern, text, re.IGNORECASE):
            # There's likely experience content, but we can't reliably extract it
            logger.debug("Experience content detected but no clear section header")

        # Check for education-like patterns (degree names)
        education_pattern = r"(?:bachelor|master|phd|doctorate|associate|b\.?s\.?|m\.?s\.?|m\.?b\.?a\.?)"
        if re.search(education_pattern, text, re.IGNORECASE):
            logger.debug("Education content detected but no clear section header")

        return sections

    def get_section_names(self) -> list[str]:
        """
        Get list of all recognized section names.

        Returns:
            List of section name strings.
        """
        return list(self.patterns.keys())

    def add_pattern(self, section_name: str, pattern: str) -> None:
        """
        Add a custom pattern for a section.

        Args:
            section_name: Name of the section.
            pattern: Regex pattern string.
        """
        if section_name not in self.patterns:
            self.patterns[section_name] = []
            self._compiled_patterns[section_name] = []

        self.patterns[section_name].append(pattern)
        self._compiled_patterns[section_name].append(
            re.compile(rf"^\s*{pattern}\s*:?\s*$", re.IGNORECASE)
        )
