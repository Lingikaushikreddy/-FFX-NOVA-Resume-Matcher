"""
Text processing utilities for resume parsing.

This module provides helper functions for cleaning and normalizing
text extracted from resumes.
"""

import re
from typing import Optional


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.

    Performs the following operations:
    - Removes excessive whitespace
    - Normalizes line endings
    - Removes special characters that commonly appear from PDF extraction
    - Strips leading/trailing whitespace

    Args:
        text: Raw text to clean.

    Returns:
        Cleaned and normalized text.
    """
    if not text:
        return ""

    # Replace various unicode whitespace with regular space
    text = re.sub(r"[\xa0\u200b\u2003\u2002\u2009]", " ", text)

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove excessive spaces (more than 2 consecutive)
    text = re.sub(r" {2,}", " ", text)

    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)

    return text.strip()


def normalize_whitespace(text: str) -> str:
    """
    Collapse all whitespace to single spaces.

    Args:
        text: Text to normalize.

    Returns:
        Text with normalized whitespace.
    """
    if not text:
        return ""
    return " ".join(text.split())


def extract_lines(text: str) -> list[str]:
    """
    Split text into non-empty lines.

    Args:
        text: Text to split.

    Returns:
        List of non-empty lines.
    """
    if not text:
        return []
    return [line.strip() for line in text.split("\n") if line.strip()]


def find_pattern_matches(
    text: str, pattern: str, flags: int = re.IGNORECASE
) -> list[str]:
    """
    Find all matches for a regex pattern in text.

    Args:
        text: Text to search.
        pattern: Regex pattern to match.
        flags: Regex flags (default: case-insensitive).

    Returns:
        List of matched strings.
    """
    if not text or not pattern:
        return []
    try:
        return re.findall(pattern, text, flags)
    except re.error:
        return []


def extract_between_markers(
    text: str, start_marker: str, end_marker: Optional[str] = None
) -> Optional[str]:
    """
    Extract text between two markers.

    Args:
        text: Text to search.
        start_marker: Beginning marker string.
        end_marker: Ending marker string (None means extract to end).

    Returns:
        Extracted text or None if start marker not found.
    """
    if not text or not start_marker:
        return None

    start_idx = text.lower().find(start_marker.lower())
    if start_idx == -1:
        return None

    start_idx += len(start_marker)

    if end_marker:
        end_idx = text.lower().find(end_marker.lower(), start_idx)
        if end_idx == -1:
            return text[start_idx:].strip()
        return text[start_idx:end_idx].strip()

    return text[start_idx:].strip()


def remove_bullets_and_numbering(text: str) -> str:
    """
    Remove common bullet points and list numbering.

    Args:
        text: Text containing bullets or numbers.

    Returns:
        Text with bullets and numbering removed.
    """
    if not text:
        return ""

    # Common bullet characters
    bullet_pattern = r"^[\s]*[•●○◦▪▸►\-\*\+]\s*"
    # Numbered lists like "1.", "1)", "(1)", "a.", "a)"
    number_pattern = r"^[\s]*(\d+[\.\)]\s*|\(\d+\)\s*|[a-zA-Z][\.\)]\s*)"

    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        line = re.sub(bullet_pattern, "", line)
        line = re.sub(number_pattern, "", line)
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def is_likely_header(text: str) -> bool:
    """
    Determine if a line is likely a section header.

    Headers typically:
    - Are short (less than 50 characters)
    - May be all uppercase
    - Don't end with common sentence punctuation
    - May end with a colon

    Args:
        text: Line to check.

    Returns:
        True if line appears to be a header.
    """
    if not text:
        return False

    text = text.strip()

    # Too long for a header
    if len(text) > 50:
        return False

    # Ends with sentence punctuation (not a header)
    if text.endswith((".", "!", "?")):
        return False

    # All uppercase or title case with colon
    if text.isupper() or text.endswith(":"):
        return True

    # Title case check
    words = text.split()
    if len(words) <= 4:
        title_case_words = sum(1 for w in words if w[0].isupper())
        if title_case_words == len(words):
            return True

    return False


def parse_date_string(date_str: str) -> Optional[str]:
    """
    Attempt to parse a date string into a standardized format.

    Handles common resume date formats:
    - "January 2020"
    - "Jan 2020"
    - "01/2020"
    - "2020"
    - "Present", "Current"

    Args:
        date_str: Date string to parse.

    Returns:
        Standardized date string or original if parsing fails.
    """
    if not date_str:
        return None

    date_str = date_str.strip()

    # Check for "present" or "current"
    if date_str.lower() in ("present", "current", "now", "ongoing"):
        return "Present"

    # Return as-is for now (could use dateutil for more robust parsing)
    return date_str


def split_date_range(date_range: str) -> tuple[Optional[str], Optional[str]]:
    """
    Split a date range string into start and end dates.

    Handles formats like:
    - "Jan 2020 - Dec 2022"
    - "2020 - Present"
    - "January 2020 to December 2022"

    Args:
        date_range: Date range string.

    Returns:
        Tuple of (start_date, end_date).
    """
    if not date_range:
        return None, None

    # Common separators for date ranges
    separators = [" - ", " – ", " to ", " through ", " until ", "-", "–"]

    for sep in separators:
        if sep in date_range:
            parts = date_range.split(sep, 1)
            if len(parts) == 2:
                start = parse_date_string(parts[0])
                end = parse_date_string(parts[1])
                return start, end

    # Single date (might be just the end date)
    return None, parse_date_string(date_range)
