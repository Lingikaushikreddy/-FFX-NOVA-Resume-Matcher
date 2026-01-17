"""
FFX NOVA Job Matcher - Main matching engine.

Combines semantic similarity, skill matching, and experience scoring
for comprehensive job-resume matching with FFX-Score algorithm.
"""

from typing import List, Optional, Union
import logging

from job_matcher.models.job import Job, ClearanceLevel
from job_matcher.models.match_result import MatchResult, SkillGap, UPSKILLING_RECOMMENDATIONS
from job_matcher.scoring.semantic_scorer import SemanticScorer
from job_matcher.scoring.skill_scorer import SkillScorer
from job_matcher.scoring.experience_scorer import ExperienceScorer
from job_matcher.utils.clearance import (
    detect_clearance_from_text,
    meets_clearance_requirement,
    clearance_to_string,
)
from job_matcher.utils.skill_synonyms import get_canonical_skill

logger = logging.getLogger(__name__)


class JobMatcher:
    """
    FFX NOVA Job Matcher with enhanced scoring algorithm.

    Implements the FFX-Score algorithm:
    FFX-Score = (0.4 × Semantic) + (0.4 × Skills) + (0.2 × Experience)

    Features:
    - Semantic similarity using sentence-transformers
    - Skill matching with synonym handling
    - Experience scoring
    - Security clearance filtering (hard requirement)
    - Upskilling recommendations for skill gaps

    Example:
        >>> from job_matcher import JobMatcher, Job
        >>> from resume_parser import parse_resume
        >>>
        >>> matcher = JobMatcher()
        >>> resume = parse_resume("resume.pdf")
        >>> job = Job(
        ...     title="Senior Python Developer",
        ...     company="TechCorp",
        ...     required_skills=["Python", "Django"],
        ...     min_experience_years=5,
        ... )
        >>> result = matcher.match(resume, job)
        >>> print(f"FFX-Score: {result.score:.1f}")
    """

    # FFX-Score weights
    SEMANTIC_WEIGHT = 0.4
    SKILL_WEIGHT = 0.4
    EXPERIENCE_WEIGHT = 0.2

    def __init__(
        self,
        semantic_weight: float = 0.4,
        skill_weight: float = 0.4,
        experience_weight: float = 0.2,
    ):
        """
        Initialize job matcher.

        Args:
            semantic_weight: Weight for semantic similarity (default 0.4).
            skill_weight: Weight for skill matching (default 0.4).
            experience_weight: Weight for experience (default 0.2).

        Raises:
            ValueError: If weights don't sum to 1.0.
        """
        total = semantic_weight + skill_weight + experience_weight
        if not abs(total - 1.0) < 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")

        self.semantic_weight = semantic_weight
        self.skill_weight = skill_weight
        self.experience_weight = experience_weight

        # Initialize scorers
        self.semantic_scorer = SemanticScorer()
        self.skill_scorer = SkillScorer()
        self.experience_scorer = ExperienceScorer()

    def match(
        self,
        resume: "Resume",
        job: Job,
        resume_embedding: Optional[List[float]] = None,
        job_embedding: Optional[List[float]] = None,
    ) -> MatchResult:
        """
        Calculate match score between resume and job.

        Args:
            resume: Resume object from resume_parser.
            job: Job object with requirements.
            resume_embedding: Pre-computed resume embedding (optional).
            job_embedding: Pre-computed job embedding (optional).

        Returns:
            MatchResult with FFX-Score and explanations.
        """
        logger.debug(f"Matching resume against job: {job.title} @ {job.company}")

        # Extract resume data
        resume_text = getattr(resume, "raw_text", "")
        resume_skills = getattr(resume, "skills", [])
        resume_experience = getattr(resume, "experience", [])

        # Detect resume clearance level
        resume_clearance = detect_clearance_from_text(resume_text)

        # 1. Clearance filter (hard requirement)
        if not meets_clearance_requirement(resume_clearance, job.clearance_level):
            return MatchResult(
                score=0.0,
                disqualified=True,
                disqualification_reason=(
                    f"Clearance requirement not met. "
                    f"Job requires {clearance_to_string(job.clearance_level)}, "
                    f"resume shows {clearance_to_string(resume_clearance)}."
                ),
                clearance_met=False,
                job_id=job.job_id,
                job_title=job.title,
                job_company=job.company,
            )

        # 2. Calculate semantic similarity
        semantic_score = self.semantic_scorer.score(
            resume_text=resume_text,
            job_text=job.description,
            resume_embedding=resume_embedding,
            job_embedding=job_embedding,
        )

        # 3. Calculate skill match
        skill_result = self.skill_scorer.score(
            resume_skills=resume_skills,
            required_skills=job.required_skills,
            preferred_skills=job.preferred_skills,
        )

        # 4. Calculate experience score
        resume_years = self._estimate_experience_years(resume)
        experience_score = self.experience_scorer.score(
            resume_years=resume_years,
            job_min_years=job.min_experience_years,
            experience_entries=[
                {"start_date": exp.start_date, "end_date": exp.end_date, "is_current": exp.is_current}
                for exp in resume_experience
            ] if resume_experience else None,
        )

        # 5. Calculate FFX-Score (0-100 scale)
        ffx_score = (
            self.semantic_weight * semantic_score +
            self.skill_weight * skill_result.score +
            self.experience_weight * experience_score
        ) * 100

        # 6. Generate upskilling recommendations
        upskilling = self._get_upskilling_recommendations(
            skill_result.missing_required + skill_result.missing_preferred
        )

        # 7. Build result
        result = MatchResult(
            score=round(ffx_score, 1),
            semantic_score=round(semantic_score, 4),
            skill_score=round(skill_result.score, 4),
            experience_score=round(experience_score, 4),
            matched_skills=skill_result.matched_skills,
            missing_required_skills=skill_result.missing_required,
            missing_preferred_skills=skill_result.missing_preferred,
            skill_gaps=skill_result.gaps,
            upskilling_recommendations=upskilling,
            clearance_met=True,
            job_id=job.job_id,
            job_title=job.title,
            job_company=job.company,
        )

        # Generate explanation
        result.explanation = result.generate_explanation()

        logger.debug(
            f"Match result: FFX-Score={result.score:.1f}, "
            f"semantic={semantic_score:.2f}, skill={skill_result.score:.2f}, "
            f"exp={experience_score:.2f}"
        )

        return result

    def match_batch(
        self,
        resume: "Resume",
        jobs: List[Job],
        resume_embedding: Optional[List[float]] = None,
        sort_by_score: bool = True,
    ) -> List[MatchResult]:
        """
        Match resume against multiple jobs efficiently.

        Args:
            resume: Resume object.
            jobs: List of Job objects.
            resume_embedding: Pre-computed resume embedding (optional).
            sort_by_score: Whether to sort results by score descending.

        Returns:
            List of MatchResult objects.
        """
        if not jobs:
            return []

        logger.info(f"Batch matching resume against {len(jobs)} jobs")

        # Pre-compute resume embedding for efficiency
        if resume_embedding is None:
            resume_text = getattr(resume, "raw_text", "")
            if resume_text:
                resume_embedding = self.semantic_scorer.embedding_service.encode(resume_text)

        results = []
        for job in jobs:
            result = self.match(resume, job, resume_embedding=resume_embedding)
            results.append(result)

        if sort_by_score:
            results.sort(key=lambda r: r.score, reverse=True)

        return results

    def get_top_matches(
        self,
        resume: "Resume",
        jobs: List[Job],
        top_k: int = 10,
        min_score: float = 0.0,
        require_clearance: bool = True,
    ) -> List[MatchResult]:
        """
        Get top K matching jobs for a resume.

        Args:
            resume: Resume object.
            jobs: List of Job objects to match against.
            top_k: Number of top matches to return.
            min_score: Minimum FFX-Score to include.
            require_clearance: Whether to filter out clearance disqualifications.

        Returns:
            List of top K MatchResult objects.
        """
        all_results = self.match_batch(resume, jobs, sort_by_score=True)

        # Filter results
        filtered = []
        for result in all_results:
            if require_clearance and result.disqualified:
                continue
            if result.score >= min_score:
                filtered.append(result)

        return filtered[:top_k]

    def _estimate_experience_years(self, resume: "Resume") -> Optional[float]:
        """
        Estimate years of experience from resume.

        Args:
            resume: Resume object.

        Returns:
            Estimated years or None.
        """
        # Try to get from resume text
        resume_text = getattr(resume, "raw_text", "")
        if resume_text:
            years = self.experience_scorer.estimate_years_from_text(resume_text)
            if years is not None:
                return years

        # Fallback: estimate from number of positions
        experience = getattr(resume, "experience", [])
        if experience:
            return self.experience_scorer.estimate_from_positions(len(experience))

        return None

    def _get_upskilling_recommendations(
        self,
        missing_skills: List[str],
        max_recommendations: int = 5,
    ) -> List[str]:
        """
        Generate upskilling recommendations for missing skills.

        Args:
            missing_skills: List of missing skill names.
            max_recommendations: Maximum recommendations to return.

        Returns:
            List of recommendation strings.
        """
        recommendations = []

        for skill in missing_skills[:max_recommendations]:
            skill_lower = skill.lower()
            canonical = get_canonical_skill(skill)

            if skill_lower in UPSKILLING_RECOMMENDATIONS:
                rec = UPSKILLING_RECOMMENDATIONS[skill_lower]
                recommendations.append(
                    f"Learn {canonical}: {rec.get('learning_path', '')}"
                )
            else:
                recommendations.append(f"Develop {canonical} skills")

        return recommendations


def match_resume_to_jobs(
    resume: "Resume",
    jobs: List[Job],
    top_k: int = 10,
) -> List[MatchResult]:
    """
    Convenience function to match resume to jobs.

    Args:
        resume: Resume object from resume_parser.
        jobs: List of Job objects.
        top_k: Number of top matches to return.

    Returns:
        List of top K MatchResult objects sorted by score.

    Example:
        >>> from resume_parser import parse_resume
        >>> from job_matcher import match_resume_to_jobs, Job
        >>>
        >>> resume = parse_resume("resume.pdf")
        >>> jobs = [Job(...), Job(...)]
        >>> results = match_resume_to_jobs(resume, jobs, top_k=5)
    """
    matcher = JobMatcher()
    return matcher.get_top_matches(resume, jobs, top_k=top_k)


# Type hint for Resume (avoid circular import)
try:
    from resume_parser.models.resume import Resume
except ImportError:
    Resume = object
