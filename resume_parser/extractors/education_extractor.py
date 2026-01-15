"""
Education extraction module.

This module extracts educational background from resume text,
including degrees, institutions, graduation dates, and honors.
"""

import re
from typing import Optional
import logging

from resume_parser.models.resume import Education
from resume_parser.utils.text_utils import extract_lines

logger = logging.getLogger(__name__)


# Common degree patterns
DEGREE_PATTERNS: dict[str, list[str]] = {
    "doctorate": [
        r"Ph\.?D\.?",
        r"Doctor\s+of\s+Philosophy",
        r"Doctorate",
        r"D\.?B\.?A\.?",
        r"Doctor\s+of\s+Business\s+Administration",
        r"Ed\.?D\.?",
        r"Doctor\s+of\s+Education",
        r"J\.?D\.?",
        r"Juris\s+Doctor",
        r"M\.?D\.?",
        r"Doctor\s+of\s+Medicine",
    ],
    "masters": [
        r"Master(?:'s)?\s+(?:of\s+)?(?:Science|Arts|Business|Engineering|Education|Fine\s+Arts)",
        r"M\.?S\.?",
        r"M\.?A\.?",
        r"M\.?B\.?A\.?",
        r"M\.?Eng\.?",
        r"M\.?Ed\.?",
        r"M\.?F\.?A\.?",
        r"Master(?:'s)?\s+(?:Degree|of)",
    ],
    "bachelors": [
        r"Bachelor(?:'s)?\s+(?:of\s+)?(?:Science|Arts|Engineering|Fine\s+Arts|Business)",
        r"B\.?S\.?",
        r"B\.?A\.?",
        r"B\.?Eng\.?",
        r"B\.?F\.?A\.?",
        r"B\.?B\.?A\.?",
        r"Bachelor(?:'s)?\s+(?:Degree|of)",
    ],
    "associate": [
        r"Associate(?:'s)?\s+(?:of\s+)?(?:Science|Arts|Applied\s+Science)",
        r"A\.?S\.?",
        r"A\.?A\.?",
        r"A\.?A\.?S\.?",
        r"Associate(?:'s)?\s+Degree",
    ],
    "certificate": [
        r"Certificate",
        r"Certification",
        r"Diploma",
        r"Professional\s+Certificate",
    ],
}

# Fields of study patterns
FIELD_OF_STUDY_PATTERNS: list[str] = [
    r"(?:in|of)\s+([A-Z][a-z]+(?:\s+[A-Z]?[a-z]+)*)",
    r"(?:Major|Concentration|Focus|Specialization):\s*([A-Z][a-z]+(?:\s+[A-Z]?[a-z]+)*)",
]

# Common fields of study for matching
COMMON_FIELDS: list[str] = [
    "Computer Science", "Software Engineering", "Information Technology",
    "Data Science", "Artificial Intelligence", "Machine Learning",
    "Electrical Engineering", "Mechanical Engineering", "Civil Engineering",
    "Chemical Engineering", "Biomedical Engineering", "Aerospace Engineering",
    "Business Administration", "Finance", "Accounting", "Economics",
    "Marketing", "Management", "Human Resources", "Operations Management",
    "Mathematics", "Statistics", "Physics", "Chemistry", "Biology",
    "Psychology", "Sociology", "Political Science", "Communications",
    "English", "History", "Philosophy", "Education",
    "Nursing", "Healthcare Administration", "Public Health",
    "Law", "Criminal Justice", "Public Administration",
    "Graphic Design", "Fine Arts", "Music", "Theater",
    "Environmental Science", "Geography", "Anthropology",
]

# Graduation date patterns
GRADUATION_PATTERNS: list[str] = [
    r"(?:Graduated|Graduation|Expected|Class\s+of|Completed)?\s*:?\s*(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}",
    r"(?:Graduated|Graduation|Expected|Class\s+of|Completed)\s*:?\s*\d{4}",
    r"'\d{2}\b",  # '22 format
    r"\b\d{4}\b",  # Just year
]


class EducationExtractor:
    """
    Extract educational background from resume text.

    Parses education sections to identify degrees, institutions,
    graduation dates, GPAs, and honors.

    Example:
        extractor = EducationExtractor()
        education = extractor.extract(education_section_text)
    """

    def __init__(self) -> None:
        """Initialize the education extractor with compiled patterns."""
        self._degree_patterns: dict[str, list[re.Pattern]] = {}
        for level, patterns in DEGREE_PATTERNS.items():
            self._degree_patterns[level] = [
                re.compile(rf"\b{p}\b", re.IGNORECASE) for p in patterns
            ]

        self._field_patterns = [
            re.compile(p, re.IGNORECASE) for p in FIELD_OF_STUDY_PATTERNS
        ]
        self._graduation_patterns = [
            re.compile(p, re.IGNORECASE) for p in GRADUATION_PATTERNS
        ]

    def extract(
        self,
        text: str,
        education_section: Optional[str] = None,
    ) -> list[Education]:
        """
        Extract education entries from resume text.

        Args:
            text: Full resume text.
            education_section: Optional education section content.

        Returns:
            List of Education objects.
        """
        # Prefer education section if available
        search_text = education_section if education_section else text

        if not search_text:
            return []

        # Split into potential education blocks
        blocks = self._split_into_education_blocks(search_text)

        education_list: list[Education] = []
        for block in blocks:
            education = self._parse_education_block(block)
            if education and (education.institution or education.degree):
                education_list.append(education)

        return education_list

    def _split_into_education_blocks(self, text: str) -> list[str]:
        """
        Split education section into individual entries.

        Args:
            text: Education section text.

        Returns:
            List of text blocks, each representing one education entry.
        """
        lines = text.split("\n")
        blocks: list[str] = []
        current_block: list[str] = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this line starts a new education block
            # (contains a degree or looks like an institution)
            is_new_block = False

            # Check for degree patterns
            for patterns in self._degree_patterns.values():
                for pattern in patterns:
                    if pattern.search(line):
                        if current_block:
                            is_new_block = True
                        break

            if is_new_block and current_block:
                blocks.append("\n".join(current_block))
                current_block = []

            current_block.append(line)

        if current_block:
            blocks.append("\n".join(current_block))

        return blocks

    def _parse_education_block(self, block: str) -> Optional[Education]:
        """
        Parse a single education block into Education object.

        Args:
            block: Text block for one education entry.

        Returns:
            Education object, or None if parsing fails.
        """
        if not block:
            return None

        education = Education()

        # Extract degree
        degree_info = self._extract_degree(block)
        if degree_info:
            education.degree = degree_info

        # Extract field of study
        education.field_of_study = self._extract_field_of_study(block)

        # Extract institution
        education.institution = self._extract_institution(block)

        # Extract graduation date
        education.graduation_date = self._extract_graduation_date(block)

        # Extract GPA
        education.gpa = self._extract_gpa(block)

        # Extract honors
        education.honors = self._extract_honors(block)

        return education

    def _extract_degree(self, text: str) -> Optional[str]:
        """
        Extract degree type from text.

        Args:
            text: Education block text.

        Returns:
            Degree string, or None.
        """
        # Check each degree level (highest first)
        for level in ["doctorate", "masters", "bachelors", "associate", "certificate"]:
            for pattern in self._degree_patterns[level]:
                match = pattern.search(text)
                if match:
                    return match.group()

        return None

    def _extract_field_of_study(self, text: str) -> Optional[str]:
        """
        Extract field of study from text.

        Args:
            text: Education block text.

        Returns:
            Field of study string, or None.
        """
        # First try pattern matching
        for pattern in self._field_patterns:
            match = pattern.search(text)
            if match:
                field = match.group(1).strip()
                return field

        # Then look for known fields
        for field in COMMON_FIELDS:
            if re.search(rf"\b{re.escape(field)}\b", text, re.IGNORECASE):
                return field

        return None

    def _extract_institution(self, text: str) -> Optional[str]:
        """
        Extract institution name from text.

        Args:
            text: Education block text.

        Returns:
            Institution name, or None.
        """
        lines = extract_lines(text)

        # Common institution indicators
        institution_patterns = [
            r"(?:University|College|Institute|School|Academy)\s+(?:of\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*",
            r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:University|College|Institute|School|Academy)",
            r"[A-Z]{2,}(?:\s+[A-Z][a-z]+)*",  # Acronyms like MIT, UCLA
        ]

        for pattern in institution_patterns:
            match = re.search(pattern, text)
            if match:
                institution = match.group()
                # Verify it's not a degree
                is_degree = False
                for patterns in self._degree_patterns.values():
                    for deg_pattern in patterns:
                        if deg_pattern.fullmatch(institution):
                            is_degree = True
                            break
                if not is_degree:
                    return institution

        # Fallback: first line that doesn't look like a degree
        for line in lines:
            line = line.strip()
            is_degree = False
            for patterns in self._degree_patterns.values():
                for pattern in patterns:
                    if pattern.search(line):
                        is_degree = True
                        break

            if not is_degree and len(line) > 3:
                # Remove dates
                for pattern in self._graduation_patterns:
                    line = pattern.sub("", line).strip()
                if line:
                    return line

        return None

    def _extract_graduation_date(self, text: str) -> Optional[str]:
        """
        Extract graduation date from text.

        Args:
            text: Education block text.

        Returns:
            Graduation date string, or None.
        """
        for pattern in self._graduation_patterns:
            match = pattern.search(text)
            if match:
                date = match.group().strip()
                # Clean up common prefixes
                date = re.sub(
                    r"^(?:Graduated|Graduation|Expected|Class\s+of|Completed)\s*:?\s*",
                    "",
                    date,
                    flags=re.IGNORECASE,
                ).strip()
                return date

        return None

    def _extract_gpa(self, text: str) -> Optional[str]:
        """
        Extract GPA from text.

        Args:
            text: Education block text.

        Returns:
            GPA string, or None.
        """
        gpa_patterns = [
            r"GPA\s*:?\s*(\d+\.?\d*)\s*(?:/\s*\d+\.?\d*)?",
            r"Grade\s+Point\s+Average\s*:?\s*(\d+\.?\d*)",
            r"(\d+\.\d+)\s*/\s*4\.0",
        ]

        for pattern in gpa_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def _extract_honors(self, text: str) -> Optional[str]:
        """
        Extract honors and distinctions from text.

        Args:
            text: Education block text.

        Returns:
            Honors string, or None.
        """
        honors_patterns = [
            r"(?:Summa|Magna|Cum)\s+Laude",
            r"Dean'?s?\s+List",
            r"(?:High\s+)?Honor(?:s|'s)?\s*(?:List|Roll|Society)?",
            r"Valedictorian|Salutatorian",
            r"With\s+(?:High\s+)?Distinction",
            r"Phi\s+Beta\s+Kappa",
        ]

        found_honors: list[str] = []
        for pattern in honors_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                found_honors.append(match.group())

        return ", ".join(found_honors) if found_honors else None
