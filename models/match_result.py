"""
Match result models with explainability.

Provides detailed scoring and explanation for resume-job matches.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
import json


@dataclass
class SkillMatch:
    """
    Individual skill matching information.

    Attributes:
        skill: The skill name.
        matched: Whether the resume has this skill.
        category: Skill category if known.
        is_required: Whether this is a required skill.
    """

    skill: str = ""
    matched: bool = False
    category: Optional[str] = None
    is_required: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ExplainabilityData:
    """
    Detailed explanation of match score components.

    Provides transparency into how the match score was calculated.

    Attributes:
        matched_skills: Skills found in both resume and job.
        missing_required_skills: Required skills not found in resume.
        missing_preferred_skills: Preferred skills not found in resume.
        skill_match_percentage: Percentage of skills matched (0-100).
        semantic_similarity: Semantic similarity score (0-1).
        experience_match: Description of experience match status.
        education_match: Description of education match status.
        explanation_text: Human-readable explanation.
    """

    matched_skills: list[str] = field(default_factory=list)
    missing_required_skills: list[str] = field(default_factory=list)
    missing_preferred_skills: list[str] = field(default_factory=list)
    skill_match_percentage: float = 0.0
    semantic_similarity: float = 0.0
    experience_match: Optional[str] = None
    education_match: Optional[str] = None
    explanation_text: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    def generate_explanation(self) -> str:
        """
        Generate human-readable explanation of the match.

        Returns:
            Explanation text.
        """
        parts = []

        # Skills summary
        if self.matched_skills:
            parts.append(
                f"Matched {len(self.matched_skills)} skills: "
                f"{', '.join(self.matched_skills[:5])}"
                f"{'...' if len(self.matched_skills) > 5 else ''}"
            )

        if self.missing_required_skills:
            parts.append(
                f"Missing {len(self.missing_required_skills)} required skills: "
                f"{', '.join(self.missing_required_skills[:3])}"
                f"{'...' if len(self.missing_required_skills) > 3 else ''}"
            )

        # Semantic match
        if self.semantic_similarity >= 0.8:
            parts.append("Strong semantic match with job description.")
        elif self.semantic_similarity >= 0.6:
            parts.append("Good semantic match with job description.")
        elif self.semantic_similarity >= 0.4:
            parts.append("Moderate semantic match with job description.")

        # Experience
        if self.experience_match:
            parts.append(self.experience_match)

        # Education
        if self.education_match:
            parts.append(self.education_match)

        return " ".join(parts) if parts else "No detailed explanation available."


@dataclass
class MatchResult:
    """
    Complete matching result with scores and explainability.

    This is the main output of the matching algorithm.

    Attributes:
        resume_id: ID of the matched resume.
        job_id: ID of the matched job.
        final_score: Weighted final match score (0-1).
        semantic_score: Semantic similarity component (0-1).
        skill_score: Skill matching component (0-1).
        semantic_weight: Weight used for semantic score.
        skill_weight: Weight used for skill score.
        explainability: Detailed explanation of the match.
        match_id: Unique identifier for this match result.
        created_at: Timestamp when match was calculated.
    """

    resume_id: Optional[str] = None
    job_id: Optional[str] = None
    final_score: float = 0.0
    semantic_score: float = 0.0
    skill_score: float = 0.0
    semantic_weight: float = 0.4
    skill_weight: float = 0.6
    explainability: ExplainabilityData = field(default_factory=ExplainabilityData)
    match_id: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        result = asdict(self)
        return result

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def get_score_breakdown(self) -> dict:
        """
        Get detailed score breakdown.

        Returns:
            Dictionary with score components and weights.
        """
        return {
            "final_score": round(self.final_score * 100, 1),
            "semantic_score": round(self.semantic_score * 100, 1),
            "skill_score": round(self.skill_score * 100, 1),
            "semantic_contribution": round(
                self.semantic_score * self.semantic_weight * 100, 1
            ),
            "skill_contribution": round(
                self.skill_score * self.skill_weight * 100, 1
            ),
        }

    def is_strong_match(self, threshold: float = 0.7) -> bool:
        """
        Check if this is a strong match.

        Args:
            threshold: Minimum score to be considered strong.

        Returns:
            True if final_score >= threshold.
        """
        return self.final_score >= threshold

    def get_match_tier(self) -> str:
        """
        Get match quality tier.

        Returns:
            String indicating match quality.
        """
        if self.final_score >= 0.85:
            return "Excellent"
        elif self.final_score >= 0.70:
            return "Strong"
        elif self.final_score >= 0.55:
            return "Good"
        elif self.final_score >= 0.40:
            return "Fair"
        else:
            return "Weak"
