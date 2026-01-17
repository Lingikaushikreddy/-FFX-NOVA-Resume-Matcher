"""
FFX NOVA Job Matcher - Enhanced job matching with FFX-Score algorithm.

This module provides AI-powered job matching for Northern Virginia's
workforce, supporting federal workers, military personnel, and contractors.

Features:
- FFX-Score algorithm (semantic + skills + experience)
- Security clearance support (None, Secret, Top Secret, TS/SCI)
- Skill synonym handling
- Upskilling recommendations
- Fast batch matching
"""

from job_matcher.matcher import JobMatcher, match_resume_to_jobs
from job_matcher.models.job import Job, ClearanceLevel
from job_matcher.models.match_result import MatchResult, SkillGap

__all__ = [
    "JobMatcher",
    "match_resume_to_jobs",
    "Job",
    "ClearanceLevel",
    "MatchResult",
    "SkillGap",
]

__version__ = "1.0.0"
