"""
Requirement extraction for job descriptions.

Extracts structured requirements including education,
experience, and other qualifications.
"""

import re
from typing import Optional
import logging

from models.job import JobRequirement

logger = logging.getLogger(__name__)


class RequirementExtractor:
    """
    Extract structured requirements from job descriptions.

    Identifies education requirements, experience levels,
    and other qualifications.

    Example:
        extractor = RequirementExtractor()
        requirements = extractor.extract(job_text)
    """

    # Education keywords
    EDUCATION_KEYWORDS = [
        "bachelor",
        "master",
        "phd",
        "doctorate",
        "degree",
        "diploma",
        "bs",
        "ba",
        "ms",
        "ma",
        "mba",
        "undergraduate",
        "graduate",
        "associate",
        "certification",
        "certified",
    ]

    # Experience patterns
    EXPERIENCE_PATTERNS = [
        r"(\d+)\+?\s*years?\s+(?:of\s+)?experience",
        r"experience[:\s]+(\d+)\+?\s*years?",
        r"minimum\s+(?:of\s+)?(\d+)\s*years?",
        r"at\s+least\s+(\d+)\s*years?",
        r"(\d+)-(\d+)\s*years?\s+(?:of\s+)?experience",
    ]

    def __init__(self):
        """Initialize the requirement extractor."""
        self._experience_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.EXPERIENCE_PATTERNS
        ]

    def extract(self, text: str) -> list[JobRequirement]:
        """
        Extract all requirements from job text.

        Args:
            text: Job description text.

        Returns:
            List of JobRequirement objects.
        """
        requirements = []

        # Extract education requirements
        requirements.extend(self._extract_education(text))

        # Extract experience requirements
        requirements.extend(self._extract_experience(text))

        return requirements

    def extract_experience_years(self, text: str) -> Optional[tuple[int, Optional[int]]]:
        """
        Extract experience years requirement.

        Args:
            text: Job description text.

        Returns:
            Tuple of (min_years, max_years) or None if not found.
        """
        for pattern in self._experience_patterns:
            match = pattern.search(text)
            if match:
                groups = match.groups()
                if len(groups) == 2 and groups[1]:
                    # Range pattern (e.g., "3-5 years")
                    return int(groups[0]), int(groups[1])
                else:
                    # Single value (e.g., "5+ years")
                    return int(groups[0]), None

        return None

    def _extract_education(self, text: str) -> list[JobRequirement]:
        """
        Extract education requirements.

        Args:
            text: Job description text.

        Returns:
            List of education JobRequirement objects.
        """
        education_reqs = []
        sentences = re.split(r"[.!?]", text)

        for sentence in sentences:
            sentence_lower = sentence.lower()
            for keyword in self.EDUCATION_KEYWORDS:
                if keyword in sentence_lower:
                    # Check if this is actually a requirement
                    if self._is_requirement_context(sentence):
                        req = JobRequirement(
                            requirement_type="required",
                            description=sentence.strip(),
                            category="education",
                        )
                        education_reqs.append(req)
                        break

        return education_reqs

    def _extract_experience(self, text: str) -> list[JobRequirement]:
        """
        Extract experience requirements.

        Args:
            text: Job description text.

        Returns:
            List of experience JobRequirement objects.
        """
        experience_reqs = []

        for pattern in self._experience_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                # Get surrounding context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()

                req = JobRequirement(
                    requirement_type="required",
                    description=context,
                    category="experience",
                )
                experience_reqs.append(req)

        return experience_reqs

    def _is_requirement_context(self, text: str) -> bool:
        """
        Check if text appears to be stating a requirement.

        Args:
            text: Text to check.

        Returns:
            True if text appears to be a requirement.
        """
        text_lower = text.lower()

        # Positive indicators
        requirement_words = [
            "required",
            "require",
            "must",
            "should",
            "need",
            "prefer",
            "minimum",
            "at least",
            "looking for",
            "seeking",
        ]

        # Negative indicators (not a requirement)
        exclusion_words = [
            "we offer",
            "we provide",
            "you will learn",
            "training provided",
        ]

        for word in exclusion_words:
            if word in text_lower:
                return False

        for word in requirement_words:
            if word in text_lower:
                return True

        # Default to True for education/experience context
        return True

    def extract_location_requirements(self, text: str) -> dict:
        """
        Extract location-related requirements.

        Args:
            text: Job description text.

        Returns:
            Dictionary with location info.
        """
        text_lower = text.lower()

        is_remote = any(
            word in text_lower
            for word in ["remote", "work from home", "wfh", "fully remote"]
        )

        is_hybrid = any(
            word in text_lower for word in ["hybrid", "flexible location"]
        )

        is_onsite = any(
            word in text_lower for word in ["on-site", "onsite", "in-office"]
        )

        return {
            "is_remote": is_remote,
            "is_hybrid": is_hybrid,
            "is_onsite": is_onsite,
        }
