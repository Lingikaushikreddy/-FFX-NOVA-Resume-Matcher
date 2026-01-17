"""
Skill matching scorer with synonym handling.

Calculates skill overlap between resume and job requirements,
using synonym mapping for accurate matching.
"""

from dataclasses import dataclass, field
from typing import List, Set
import logging

from job_matcher.utils.skill_synonyms import (
    normalize_skill,
    get_canonical_skill,
)
from job_matcher.models.match_result import SkillGap

logger = logging.getLogger(__name__)


@dataclass
class SkillMatchResult:
    """
    Result of skill matching analysis.

    Attributes:
        score: Skill match score (0-1).
        matched_skills: Skills found in both resume and job.
        missing_required: Required skills not in resume.
        missing_preferred: Preferred skills not in resume.
        gaps: Detailed skill gap analysis.
    """

    score: float = 0.0
    matched_skills: List[str] = field(default_factory=list)
    missing_required: List[str] = field(default_factory=list)
    missing_preferred: List[str] = field(default_factory=list)
    gaps: List[SkillGap] = field(default_factory=list)


class SkillScorer:
    """
    Skill matching scorer with synonym support.

    Uses weighted scoring where required skills are worth
    2x as much as preferred skills.

    Example:
        >>> scorer = SkillScorer()
        >>> result = scorer.score(
        ...     resume_skills=["Python", "Django", "AWS"],
        ...     required_skills=["Python", "PostgreSQL"],
        ...     preferred_skills=["Docker"],
        ... )
        >>> print(f"Skill score: {result.score:.2f}")
    """

    def __init__(self, required_weight: float = 2.0, preferred_weight: float = 1.0):
        """
        Initialize skill scorer.

        Args:
            required_weight: Weight multiplier for required skills.
            preferred_weight: Weight multiplier for preferred skills.
        """
        self.required_weight = required_weight
        self.preferred_weight = preferred_weight

    def score(
        self,
        resume_skills: List[str],
        required_skills: List[str],
        preferred_skills: List[str],
    ) -> SkillMatchResult:
        """
        Calculate skill match score with detailed breakdown.

        Uses Jaccard-style scoring with weighting:
        - Required skills matched × 2 points each
        - Preferred skills matched × 1 point each
        - Score = matched_points / total_possible_points

        Args:
            resume_skills: Skills from resume.
            required_skills: Required skills from job.
            preferred_skills: Preferred/nice-to-have skills from job.

        Returns:
            SkillMatchResult with score and details.
        """
        # Normalize all skills for comparison
        resume_normalized = {normalize_skill(s) for s in resume_skills if s}
        required_normalized = {normalize_skill(s) for s in required_skills if s}
        preferred_normalized = {normalize_skill(s) for s in preferred_skills if s}

        # Find matches
        matched_required_norm = resume_normalized & required_normalized
        matched_preferred_norm = resume_normalized & preferred_normalized

        # Find missing
        missing_required_norm = required_normalized - matched_required_norm
        missing_preferred_norm = preferred_normalized - matched_preferred_norm

        # Calculate score
        total_possible = (
            len(required_normalized) * self.required_weight +
            len(preferred_normalized) * self.preferred_weight
        )

        if total_possible == 0:
            # No skills specified in job
            score = 0.5  # Neutral score
        else:
            matched_points = (
                len(matched_required_norm) * self.required_weight +
                len(matched_preferred_norm) * self.preferred_weight
            )
            score = matched_points / total_possible

        # Build display-friendly skill lists (original casing)
        matched_skills = self._get_display_skills(
            matched_required_norm | matched_preferred_norm,
            required_skills + preferred_skills,
        )
        missing_required = self._get_display_skills(
            missing_required_norm,
            required_skills,
        )
        missing_preferred = self._get_display_skills(
            missing_preferred_norm,
            preferred_skills,
        )

        # Build skill gaps
        gaps = self._build_skill_gaps(missing_required, missing_preferred)

        return SkillMatchResult(
            score=min(score, 1.0),
            matched_skills=sorted(matched_skills),
            missing_required=sorted(missing_required),
            missing_preferred=sorted(missing_preferred),
            gaps=gaps,
        )

    def _get_display_skills(
        self,
        normalized_skills: Set[str],
        original_skills: List[str],
    ) -> List[str]:
        """
        Get display-friendly skill names from normalized set.

        Tries to preserve original casing from job posting.
        """
        display = []
        seen = set()

        for skill in original_skills:
            norm = normalize_skill(skill)
            if norm in normalized_skills and norm not in seen:
                display.append(get_canonical_skill(skill))
                seen.add(norm)

        return display

    def _build_skill_gaps(
        self,
        missing_required: List[str],
        missing_preferred: List[str],
    ) -> List[SkillGap]:
        """Build SkillGap objects for missing skills."""
        gaps = []

        for skill in missing_required:
            gaps.append(SkillGap(
                skill=skill,
                importance="required",
                category=self._categorize_skill(skill),
            ))

        for skill in missing_preferred:
            gaps.append(SkillGap(
                skill=skill,
                importance="preferred",
                category=self._categorize_skill(skill),
            ))

        return gaps

    def _categorize_skill(self, skill: str) -> str:
        """Categorize a skill into a general category."""
        skill_lower = skill.lower()

        programming = {
            "python", "java", "javascript", "typescript", "c++", "c#",
            "go", "rust", "ruby", "php", "swift", "kotlin", "scala",
        }
        frontend = {
            "react", "angular", "vue", "svelte", "html", "css",
            "tailwind", "bootstrap", "jquery",
        }
        backend = {
            "django", "flask", "fastapi", "spring", "node.js", "express",
            "rails", "laravel", "asp.net",
        }
        database = {
            "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
            "dynamodb", "cassandra", "sql", "oracle",
        }
        cloud = {
            "aws", "azure", "gcp", "heroku", "digitalocean",
        }
        devops = {
            "docker", "kubernetes", "terraform", "ansible", "jenkins",
            "ci/cd", "linux", "nginx",
        }
        data = {
            "machine learning", "deep learning", "tensorflow", "pytorch",
            "pandas", "numpy", "spark", "hadoop",
        }

        normalized = normalize_skill(skill)

        if normalized in programming:
            return "programming"
        elif normalized in frontend:
            return "frontend"
        elif normalized in backend:
            return "backend"
        elif normalized in database:
            return "database"
        elif normalized in cloud:
            return "cloud"
        elif normalized in devops:
            return "devops"
        elif normalized in data:
            return "data_science"
        else:
            return "technical"

    def get_skill_overlap_percentage(
        self,
        resume_skills: List[str],
        job_skills: List[str],
    ) -> float:
        """
        Calculate simple skill overlap percentage.

        Args:
            resume_skills: Skills from resume.
            job_skills: All skills from job (required + preferred).

        Returns:
            Percentage of job skills found in resume (0-100).
        """
        if not job_skills:
            return 0.0

        resume_normalized = {normalize_skill(s) for s in resume_skills}
        job_normalized = {normalize_skill(s) for s in job_skills}

        matched = resume_normalized & job_normalized
        return (len(matched) / len(job_normalized)) * 100
