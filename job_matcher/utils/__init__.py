"""Utility modules for job matching."""

from job_matcher.utils.clearance import (
    ClearanceLevel,
    detect_clearance_from_text,
    meets_clearance_requirement,
    clearance_to_string,
)
from job_matcher.utils.skill_synonyms import (
    normalize_skill,
    skills_match,
    get_canonical_skill,
    SKILL_SYNONYMS,
)

__all__ = [
    "ClearanceLevel",
    "detect_clearance_from_text",
    "meets_clearance_requirement",
    "clearance_to_string",
    "normalize_skill",
    "skills_match",
    "get_canonical_skill",
    "SKILL_SYNONYMS",
]
