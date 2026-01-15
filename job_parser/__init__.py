"""
Job Parser module for FFX NOVA Resume Matcher.

Provides job description parsing with skill extraction
and requirement identification.
"""

from job_parser.parser import JobParser, parse_job_text

__all__ = ["JobParser", "parse_job_text"]
