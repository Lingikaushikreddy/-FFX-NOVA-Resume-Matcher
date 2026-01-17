"""
Security clearance level handling for federal/military job matching.

Supports the standard US government clearance levels used in
Northern Virginia's defense and federal contractor ecosystem.
"""

from enum import IntEnum
import re
from typing import Optional


class ClearanceLevel(IntEnum):
    """
    US Government security clearance levels.

    Ordered by hierarchy - higher values indicate higher clearance.
    Used as hard filter: resume clearance must be >= job requirement.
    """

    NONE = 0
    PUBLIC_TRUST = 1
    SECRET = 2
    TOP_SECRET = 3
    TS_SCI = 4  # Top Secret with Sensitive Compartmented Information


# Patterns for detecting clearance from resume text
CLEARANCE_PATTERNS = {
    ClearanceLevel.TS_SCI: [
        r"\bts[/-]?sci\b",
        r"\btop\s+secret[/-]?sci\b",
        r"\bts\s+w(?:ith)?\s+sci\b",
        r"\bsci\s+clearance\b",
        r"\bsci\s+eligible\b",
    ],
    ClearanceLevel.TOP_SECRET: [
        r"\btop\s+secret\b",
        r"\bts\s+clearance\b",
        r"\bts\s+eligible\b",
        r"(?<![/-])\bts\b(?![/-])",  # TS not followed by SCI
    ],
    ClearanceLevel.SECRET: [
        r"\bsecret\s+clearance\b",
        r"\bsecret\s+eligible\b",
        r"\bactive\s+secret\b",
        r"\bcurrent\s+secret\b",
        r"(?<!top\s)\bsecret\b(?!\s+service)",  # Secret not preceded by Top
    ],
    ClearanceLevel.PUBLIC_TRUST: [
        r"\bpublic\s+trust\b",
        r"\bmoderate\s+risk\b",
        r"\bhigh\s+risk\s+public\s+trust\b",
        r"\bmbi\b",  # Moderate Background Investigation
    ],
}

# Federal/military terms that might indicate clearance context
FEDERAL_INDICATORS = [
    r"\bdod\b",
    r"\bdepartment\s+of\s+defense\b",
    r"\bdefense\s+contractor\b",
    r"\bcleared\b",
    r"\bclearance\b",
    r"\bpolygraph\b",
    r"\bfull\s+scope\s+poly\b",
    r"\bci\s+poly\b",
    r"\blifestyle\s+poly\b",
    r"\bnispom\b",
    r"\bscif\b",
]


def detect_clearance_from_text(text: str) -> ClearanceLevel:
    """
    Detect security clearance level from resume text.

    Scans text for clearance-related patterns and returns the
    highest clearance level found.

    Args:
        text: Resume or profile text to analyze.

    Returns:
        Detected ClearanceLevel (NONE if no clearance found).

    Example:
        >>> text = "Active TS/SCI clearance with CI Poly"
        >>> detect_clearance_from_text(text)
        ClearanceLevel.TS_SCI
    """
    if not text:
        return ClearanceLevel.NONE

    text_lower = text.lower()

    # Check from highest to lowest clearance
    for level in [
        ClearanceLevel.TS_SCI,
        ClearanceLevel.TOP_SECRET,
        ClearanceLevel.SECRET,
        ClearanceLevel.PUBLIC_TRUST,
    ]:
        patterns = CLEARANCE_PATTERNS.get(level, [])
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return level

    return ClearanceLevel.NONE


def meets_clearance_requirement(
    resume_clearance: ClearanceLevel,
    job_clearance: ClearanceLevel,
) -> bool:
    """
    Check if resume clearance meets job requirement.

    This is a hard filter - candidates without sufficient
    clearance cannot be considered for the position.

    Args:
        resume_clearance: Candidate's clearance level.
        job_clearance: Job's minimum clearance requirement.

    Returns:
        True if resume clearance >= job requirement.

    Example:
        >>> meets_clearance_requirement(ClearanceLevel.TOP_SECRET, ClearanceLevel.SECRET)
        True
        >>> meets_clearance_requirement(ClearanceLevel.SECRET, ClearanceLevel.TS_SCI)
        False
    """
    return resume_clearance >= job_clearance


def clearance_to_string(level: ClearanceLevel) -> str:
    """
    Convert clearance level to human-readable string.

    Args:
        level: ClearanceLevel enum value.

    Returns:
        Human-readable clearance name.
    """
    names = {
        ClearanceLevel.NONE: "None Required",
        ClearanceLevel.PUBLIC_TRUST: "Public Trust",
        ClearanceLevel.SECRET: "Secret",
        ClearanceLevel.TOP_SECRET: "Top Secret",
        ClearanceLevel.TS_SCI: "TS/SCI",
    }
    return names.get(level, "Unknown")


def parse_clearance_string(clearance_str: str) -> ClearanceLevel:
    """
    Parse a clearance string into ClearanceLevel enum.

    Args:
        clearance_str: String representation of clearance.

    Returns:
        Corresponding ClearanceLevel.
    """
    if not clearance_str:
        return ClearanceLevel.NONE

    normalized = clearance_str.lower().strip()

    mappings = {
        "none": ClearanceLevel.NONE,
        "none required": ClearanceLevel.NONE,
        "public trust": ClearanceLevel.PUBLIC_TRUST,
        "public_trust": ClearanceLevel.PUBLIC_TRUST,
        "secret": ClearanceLevel.SECRET,
        "top secret": ClearanceLevel.TOP_SECRET,
        "top_secret": ClearanceLevel.TOP_SECRET,
        "topsecret": ClearanceLevel.TOP_SECRET,
        "ts": ClearanceLevel.TOP_SECRET,
        "ts/sci": ClearanceLevel.TS_SCI,
        "ts_sci": ClearanceLevel.TS_SCI,
        "tssci": ClearanceLevel.TS_SCI,
        "sci": ClearanceLevel.TS_SCI,
    }

    return mappings.get(normalized, ClearanceLevel.NONE)


def has_federal_context(text: str) -> bool:
    """
    Check if text contains federal/military context indicators.

    Useful for determining if a resume is from someone in
    the federal/defense sector.

    Args:
        text: Text to analyze.

    Returns:
        True if federal/military indicators found.
    """
    if not text:
        return False

    text_lower = text.lower()
    for pattern in FEDERAL_INDICATORS:
        if re.search(pattern, text_lower):
            return True
    return False
