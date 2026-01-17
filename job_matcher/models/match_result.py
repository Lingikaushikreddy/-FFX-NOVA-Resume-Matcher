"""
Match result model with detailed explanations.

Provides comprehensive matching results including score breakdown,
skill gap analysis, and upskilling recommendations.
"""

from dataclasses import dataclass, field
from typing import Optional, List
import json


@dataclass
class SkillGap:
    """
    Represents a skill gap between resume and job requirements.

    Attributes:
        skill: The missing skill name.
        importance: How important this skill is (required/preferred).
        category: Skill category (programming, cloud, database, etc.).
        learning_path: Suggested way to learn this skill.
        estimated_time: Estimated time to acquire skill.
    """

    skill: str
    importance: str = "required"  # "required" or "preferred"
    category: str = "technical"
    learning_path: Optional[str] = None
    estimated_time: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "skill": self.skill,
            "importance": self.importance,
            "category": self.category,
            "learning_path": self.learning_path,
            "estimated_time": self.estimated_time,
        }


# Upskilling recommendations for common skills
UPSKILLING_RECOMMENDATIONS = {
    "kubernetes": {
        "learning_path": "Container orchestration for cloud-native applications",
        "resources": ["Kubernetes.io docs", "CKAD certification", "KodeKloud"],
        "estimated_time": "2-3 months",
    },
    "docker": {
        "learning_path": "Containerization fundamentals",
        "resources": ["Docker official docs", "Docker Captain tutorials"],
        "estimated_time": "2-4 weeks",
    },
    "aws": {
        "learning_path": "Cloud computing with Amazon Web Services",
        "resources": ["AWS Free Tier", "AWS Certified Cloud Practitioner"],
        "estimated_time": "1-2 months",
    },
    "terraform": {
        "learning_path": "Infrastructure as Code",
        "resources": ["Terraform tutorials", "HashiCorp certification"],
        "estimated_time": "3-4 weeks",
    },
    "python": {
        "learning_path": "General-purpose programming language",
        "resources": ["Python.org tutorial", "Real Python", "Codecademy"],
        "estimated_time": "2-3 months",
    },
    "react": {
        "learning_path": "Modern frontend development with React",
        "resources": ["React.dev", "Scrimba", "Frontend Masters"],
        "estimated_time": "1-2 months",
    },
    "typescript": {
        "learning_path": "Type-safe JavaScript development",
        "resources": ["TypeScript Handbook", "Execute Program"],
        "estimated_time": "2-4 weeks",
    },
    "graphql": {
        "learning_path": "Modern API query language",
        "resources": ["GraphQL.org", "Apollo tutorials"],
        "estimated_time": "2-3 weeks",
    },
    "machine learning": {
        "learning_path": "AI and statistical modeling",
        "resources": ["Coursera ML course", "fast.ai", "Kaggle"],
        "estimated_time": "3-6 months",
    },
    "postgresql": {
        "learning_path": "Advanced relational database",
        "resources": ["PostgreSQL docs", "pgexercises.com"],
        "estimated_time": "3-4 weeks",
    },
}


@dataclass
class MatchResult:
    """
    Comprehensive job match result with explanations.

    Attributes:
        score: Overall FFX-Score (0-100).
        semantic_score: Semantic similarity score (0-1).
        skill_score: Skill matching score (0-1).
        experience_score: Experience matching score (0-1).
        matched_skills: Skills that match between resume and job.
        missing_required_skills: Required skills not found in resume.
        missing_preferred_skills: Preferred skills not found in resume.
        skill_gaps: Detailed skill gap analysis.
        upskilling_recommendations: Suggestions for skill development.
        clearance_met: Whether clearance requirement is satisfied.
        disqualified: Whether candidate is disqualified (clearance).
        disqualification_reason: Reason for disqualification.
        job_title: Title of matched job.
        job_company: Company of matched job.
        explanation: Human-readable match explanation.
    """

    score: float = 0.0
    semantic_score: float = 0.0
    skill_score: float = 0.0
    experience_score: float = 0.0
    matched_skills: List[str] = field(default_factory=list)
    missing_required_skills: List[str] = field(default_factory=list)
    missing_preferred_skills: List[str] = field(default_factory=list)
    skill_gaps: List[SkillGap] = field(default_factory=list)
    upskilling_recommendations: List[str] = field(default_factory=list)
    clearance_met: bool = True
    disqualified: bool = False
    disqualification_reason: Optional[str] = None
    job_id: Optional[str] = None
    job_title: Optional[str] = None
    job_company: Optional[str] = None
    explanation: str = ""

    def get_tier(self) -> str:
        """
        Get match quality tier based on score.

        Returns:
            Match tier: Excellent, Strong, Good, Fair, or Weak.
        """
        if self.disqualified:
            return "Disqualified"
        if self.score >= 85:
            return "Excellent"
        elif self.score >= 70:
            return "Strong"
        elif self.score >= 55:
            return "Good"
        elif self.score >= 40:
            return "Fair"
        else:
            return "Weak"

    def get_score_breakdown(self) -> dict:
        """
        Get detailed score breakdown.

        Returns:
            Dictionary with score components and contributions.
        """
        return {
            "total_score": round(self.score, 1),
            "tier": self.get_tier(),
            "components": {
                "semantic": {
                    "score": round(self.semantic_score, 4),
                    "weight": 0.4,
                    "contribution": round(self.semantic_score * 0.4 * 100, 1),
                },
                "skills": {
                    "score": round(self.skill_score, 4),
                    "weight": 0.4,
                    "contribution": round(self.skill_score * 0.4 * 100, 1),
                },
                "experience": {
                    "score": round(self.experience_score, 4),
                    "weight": 0.2,
                    "contribution": round(self.experience_score * 0.2 * 100, 1),
                },
            },
            "clearance_met": self.clearance_met,
        }

    def generate_explanation(self) -> str:
        """
        Generate human-readable match explanation.

        Returns:
            Explanation text describing why this is/isn't a good match.
        """
        if self.disqualified:
            return f"Not qualified: {self.disqualification_reason}"

        lines = []

        # Overall assessment
        tier = self.get_tier()
        if tier == "Excellent":
            lines.append("Outstanding match with strong alignment across all criteria.")
        elif tier == "Strong":
            lines.append("Strong candidate with good technical and experience fit.")
        elif tier == "Good":
            lines.append("Solid match with some areas for growth.")
        elif tier == "Fair":
            lines.append("Moderate fit - may require additional training.")
        else:
            lines.append("Limited match - significant gaps identified.")

        # Skill assessment
        if self.matched_skills:
            lines.append(
                f"Matches {len(self.matched_skills)} key skills: "
                f"{', '.join(self.matched_skills[:5])}"
                f"{'...' if len(self.matched_skills) > 5 else ''}."
            )

        if self.missing_required_skills:
            lines.append(
                f"Missing {len(self.missing_required_skills)} required skills: "
                f"{', '.join(self.missing_required_skills[:3])}"
                f"{'...' if len(self.missing_required_skills) > 3 else ''}."
            )

        # Clearance note
        if self.clearance_met:
            lines.append("Meets security clearance requirements.")

        return " ".join(lines)

    def get_upskilling_details(self) -> List[dict]:
        """
        Get detailed upskilling recommendations for missing skills.

        Returns:
            List of upskilling recommendation dictionaries.
        """
        details = []
        all_missing = self.missing_required_skills + self.missing_preferred_skills

        for skill in all_missing[:5]:  # Top 5 recommendations
            skill_lower = skill.lower()
            if skill_lower in UPSKILLING_RECOMMENDATIONS:
                rec = UPSKILLING_RECOMMENDATIONS[skill_lower]
                details.append({
                    "skill": skill,
                    "importance": "required" if skill in self.missing_required_skills else "preferred",
                    "learning_path": rec.get("learning_path", ""),
                    "resources": rec.get("resources", []),
                    "estimated_time": rec.get("estimated_time", ""),
                })
            else:
                details.append({
                    "skill": skill,
                    "importance": "required" if skill in self.missing_required_skills else "preferred",
                    "learning_path": f"Develop proficiency in {skill}",
                    "resources": ["Online courses", "Documentation", "Practice projects"],
                    "estimated_time": "Varies",
                })

        return details

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "score": round(self.score, 2),
            "tier": self.get_tier(),
            "semantic_score": round(self.semantic_score, 4),
            "skill_score": round(self.skill_score, 4),
            "experience_score": round(self.experience_score, 4),
            "matched_skills": self.matched_skills,
            "missing_required_skills": self.missing_required_skills,
            "missing_preferred_skills": self.missing_preferred_skills,
            "skill_gaps": [g.to_dict() for g in self.skill_gaps],
            "upskilling_recommendations": self.upskilling_recommendations,
            "clearance_met": self.clearance_met,
            "disqualified": self.disqualified,
            "disqualification_reason": self.disqualification_reason,
            "job_id": self.job_id,
            "job_title": self.job_title,
            "job_company": self.job_company,
            "explanation": self.explanation or self.generate_explanation(),
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self) -> str:
        """String representation."""
        return f"MatchResult(score={self.score:.1f}, tier={self.get_tier()})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"MatchResult(score={self.score:.1f}, "
            f"matched_skills={len(self.matched_skills)}, "
            f"missing_required={len(self.missing_required_skills)})"
        )

    def __lt__(self, other: "MatchResult") -> bool:
        """Enable sorting by score."""
        return self.score < other.score

    def __eq__(self, other: object) -> bool:
        """Equality by score."""
        if not isinstance(other, MatchResult):
            return False
        return abs(self.score - other.score) < 0.01
