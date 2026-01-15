"""
Matching Engine module for FFX NOVA Resume Matcher.

Provides hybrid semantic-keyword matching between
resumes and jobs.
"""

from matching_engine.matcher import HybridMatcher, calculate_match

__all__ = ["HybridMatcher", "calculate_match"]
