"""
Experience scoring for job matching.

Calculates how well a candidate's experience matches
job requirements.
"""

from typing import List, Optional
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ExperienceScorer:
    """
    Experience scorer for job matching.

    Calculates experience score based on:
    - Total years of experience vs job requirement
    - Number of relevant positions

    Example:
        >>> scorer = ExperienceScorer()
        >>> score = scorer.score(
        ...     resume_years=5,
        ...     job_min_years=3,
        ... )
        >>> print(f"Experience score: {score:.2f}")  # 1.0
    """

    def score(
        self,
        resume_years: Optional[float] = None,
        job_min_years: int = 0,
        experience_entries: Optional[List[dict]] = None,
    ) -> float:
        """
        Calculate experience matching score.

        Score formula: min(resume_years / job_min_years, 1.0)
        - 1.0 if resume meets or exceeds requirement
        - Proportional score if below requirement
        - 1.0 if no requirement specified

        Args:
            resume_years: Total years of experience from resume.
            job_min_years: Minimum years required by job.
            experience_entries: List of work experience dicts (fallback).

        Returns:
            Experience score between 0 and 1.
        """
        # If no requirement, full score
        if job_min_years <= 0:
            return 1.0

        # Try to get years from provided value
        if resume_years is not None:
            years = resume_years
        # Fallback: estimate from experience entries
        elif experience_entries:
            years = self.estimate_years_from_entries(experience_entries)
        else:
            # No experience info - give partial score
            return 0.5

        # Calculate score
        if years >= job_min_years:
            return 1.0
        elif years <= 0:
            return 0.0
        else:
            return years / job_min_years

    def estimate_years_from_entries(
        self,
        entries: List[dict],
    ) -> float:
        """
        Estimate total years of experience from work entries.

        Args:
            entries: List of work experience dictionaries.

        Returns:
            Estimated years of experience.
        """
        if not entries:
            return 0.0

        total_months = 0

        for entry in entries:
            months = self._calculate_entry_duration(entry)
            total_months += months

        # Convert to years
        return total_months / 12.0

    def _calculate_entry_duration(self, entry: dict) -> int:
        """
        Calculate duration of a single work entry in months.

        Args:
            entry: Work experience dictionary.

        Returns:
            Duration in months.
        """
        start_date = entry.get("start_date")
        end_date = entry.get("end_date")
        is_current = entry.get("is_current", False)

        # Try to parse dates
        start = self._parse_date(start_date)
        end = self._parse_date(end_date)

        if start is None:
            # Use heuristic: average job tenure of 2.5 years
            return 30

        if end is None:
            if is_current:
                end = datetime.now()
            else:
                # Assume 2 years if end date missing
                return 24

        # Calculate months between dates
        months = (end.year - start.year) * 12 + (end.month - start.month)
        return max(0, months)

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """
        Parse a date string into datetime.

        Handles various formats:
        - YYYY-MM-DD
        - YYYY-MM
        - YYYY
        - Month YYYY
        - Present, Current
        """
        if not date_str:
            return None

        date_str = date_str.strip()

        # Handle "Present" or "Current"
        if date_str.lower() in ["present", "current", "now"]:
            return datetime.now()

        # Try standard formats
        formats = [
            "%Y-%m-%d",
            "%Y-%m",
            "%Y",
            "%m/%Y",
            "%m-%Y",
            "%B %Y",
            "%b %Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # Try to extract year
        year_match = re.search(r"\b(19|20)\d{2}\b", date_str)
        if year_match:
            try:
                return datetime(int(year_match.group()), 1, 1)
            except ValueError:
                pass

        return None

    def estimate_years_from_text(self, text: str) -> Optional[float]:
        """
        Extract years of experience from resume text.

        Looks for patterns like:
        - "5 years of experience"
        - "5+ years"
        - "over 5 years"

        Args:
            text: Resume text.

        Returns:
            Extracted years or None.
        """
        if not text:
            return None

        patterns = [
            # "5 years of experience"
            r"(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s*(?:experience|exp)",
            # "over 5 years"
            r"(?:over|more than|>\s*)\s*(\d+)\s*(?:years?|yrs?)",
            # "5+ years"
            r"(\d+)\+\s*(?:years?|yrs?)",
            # "experience: 5 years"
            r"(?:experience|exp)[:\s]+(\d+)\s*(?:years?|yrs?)",
        ]

        text_lower = text.lower()

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    return float(match.group(1))
                except (ValueError, IndexError):
                    continue

        return None

    def estimate_from_positions(self, num_positions: int) -> float:
        """
        Rough estimate of experience from number of positions.

        Assumes average tenure of 2.5 years per position.

        Args:
            num_positions: Number of work positions.

        Returns:
            Estimated years.
        """
        if num_positions <= 0:
            return 0.0
        return num_positions * 2.5
