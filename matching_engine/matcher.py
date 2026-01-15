"""
Hybrid semantic-keyword matching engine.

Combines vector embeddings for semantic similarity with
exact skill matching for precise, explainable results.
"""

from typing import Optional, List
import logging

from resume_parser.models.resume import Resume
from models.job import Job
from models.match_result import MatchResult, ExplainabilityData
from embeddings import get_embedding_service
from config import get_settings

logger = logging.getLogger(__name__)


class HybridMatcher:
    """
    Hybrid matching combining semantic similarity and skill matching.

    The matching algorithm uses a weighted combination of:
    - Semantic similarity (40% by default): Cosine similarity between
      resume and job embeddings, capturing conceptual matches.
    - Skill matching (60% by default): Exact skill overlap with
      required skills weighted higher than preferred.

    Example:
        matcher = HybridMatcher()
        result = matcher.match(resume, job)
        print(f"Match score: {result.final_score}")
        print(f"Matched skills: {result.explainability.matched_skills}")
    """

    def __init__(
        self,
        semantic_weight: Optional[float] = None,
        skill_weight: Optional[float] = None,
    ):
        """
        Initialize the hybrid matcher.

        Args:
            semantic_weight: Weight for semantic similarity (0-1).
            skill_weight: Weight for skill matching (0-1).

        Raises:
            ValueError: If weights don't sum to 1.0.
        """
        settings = get_settings()
        self.semantic_weight = (
            semantic_weight if semantic_weight is not None else settings.semantic_weight
        )
        self.skill_weight = (
            skill_weight if skill_weight is not None else settings.skill_weight
        )

        # Validate weights
        if not abs(self.semantic_weight + self.skill_weight - 1.0) < 0.01:
            raise ValueError(
                f"Weights must sum to 1.0. Got semantic={self.semantic_weight}, "
                f"skill={self.skill_weight}"
            )

        self.embedding_service = get_embedding_service()

    def match(
        self,
        resume: Resume,
        job: Job,
        resume_embedding: Optional[List[float]] = None,
        job_embedding: Optional[List[float]] = None,
    ) -> MatchResult:
        """
        Calculate match score between resume and job.

        Args:
            resume: Resume object with skills and raw_text.
            job: Job object with required/preferred skills.
            resume_embedding: Pre-computed resume embedding (optional).
            job_embedding: Pre-computed job embedding (optional).

        Returns:
            MatchResult with scores and explainability.
        """
        logger.debug(f"Matching resume against job: {job.title}")

        # Generate embeddings if not provided
        if resume_embedding is None:
            resume_embedding = self.embedding_service.encode(resume.raw_text)
        if job_embedding is None:
            job_embedding = self.embedding_service.encode(job.raw_text)

        # Calculate semantic similarity
        semantic_score = self.embedding_service.cosine_similarity(
            resume_embedding, job_embedding
        )

        # Calculate skill match
        skill_result = self._calculate_skill_match(resume.skills, job)
        skill_score = skill_result["score"]

        # Calculate weighted final score
        final_score = (
            self.semantic_weight * semantic_score + self.skill_weight * skill_score
        )

        # Build explainability data
        explainability = ExplainabilityData(
            matched_skills=skill_result["matched"],
            missing_required_skills=skill_result["missing_required"],
            missing_preferred_skills=skill_result["missing_preferred"],
            skill_match_percentage=round(skill_score * 100, 1),
            semantic_similarity=round(semantic_score, 4),
            experience_match=self._match_experience(resume, job),
            education_match=self._match_education(resume, job),
        )

        # Generate explanation text
        explainability.explanation_text = explainability.generate_explanation()

        # Create result
        result = MatchResult(
            final_score=round(final_score, 4),
            semantic_score=round(semantic_score, 4),
            skill_score=round(skill_score, 4),
            semantic_weight=self.semantic_weight,
            skill_weight=self.skill_weight,
            explainability=explainability,
        )

        logger.debug(
            f"Match result: final={result.final_score}, "
            f"semantic={result.semantic_score}, skill={result.skill_score}"
        )

        return result

    def match_batch(
        self,
        resume: Resume,
        jobs: List[Job],
        resume_embedding: Optional[List[float]] = None,
    ) -> List[MatchResult]:
        """
        Match a resume against multiple jobs efficiently.

        Args:
            resume: Resume to match.
            jobs: List of jobs to match against.
            resume_embedding: Pre-computed resume embedding (optional).

        Returns:
            List of MatchResult objects.
        """
        if not jobs:
            return []

        # Generate resume embedding once
        if resume_embedding is None:
            resume_embedding = self.embedding_service.encode(resume.raw_text)

        # Generate job embeddings in batch
        job_texts = [job.raw_text for job in jobs]
        job_embeddings = self.embedding_service.encode_batch(job_texts)

        # Match against each job
        results = []
        for job, job_embedding in zip(jobs, job_embeddings):
            result = self.match(
                resume, job, resume_embedding=resume_embedding, job_embedding=job_embedding
            )
            result.job_id = job.job_id
            results.append(result)

        return results

    def _calculate_skill_match(self, resume_skills: List[str], job: Job) -> dict:
        """
        Calculate skill matching score with explainability.

        Uses a weighted scoring where required skills are worth
        2x the points of preferred skills.

        Args:
            resume_skills: Skills from the resume.
            job: Job object with required/preferred skills.

        Returns:
            Dictionary with:
                - score: float (0-1)
                - matched: list of matched skills
                - missing_required: list of missing required skills
                - missing_preferred: list of missing preferred skills
        """
        # Normalize skills for comparison (lowercase)
        resume_skills_normalized = {s.lower().strip() for s in resume_skills}
        required_normalized = {s.lower().strip() for s in job.required_skills}
        preferred_normalized = {s.lower().strip() for s in job.preferred_skills}

        # Find matches
        matched_required = resume_skills_normalized & required_normalized
        matched_preferred = resume_skills_normalized & preferred_normalized

        missing_required = required_normalized - matched_required
        missing_preferred = preferred_normalized - matched_preferred

        # Calculate score
        # Required skills are worth 2 points each, preferred worth 1
        total_possible = len(required_normalized) * 2 + len(preferred_normalized)

        if total_possible == 0:
            # No skills specified in job, use semantic only (return 0.5)
            score = 0.5
        else:
            matched_points = len(matched_required) * 2 + len(matched_preferred)
            score = matched_points / total_possible

        # Get original case versions for display
        matched_display = self._get_original_case_skills(
            matched_required | matched_preferred,
            job.required_skills + job.preferred_skills,
        )
        missing_req_display = self._get_original_case_skills(
            missing_required, job.required_skills
        )
        missing_pref_display = self._get_original_case_skills(
            missing_preferred, job.preferred_skills
        )

        return {
            "score": min(score, 1.0),
            "matched": sorted(matched_display),
            "missing_required": sorted(missing_req_display),
            "missing_preferred": sorted(missing_pref_display),
        }

    def _get_original_case_skills(
        self, normalized_skills: set, original_skills: List[str]
    ) -> List[str]:
        """Get original case versions of normalized skill names."""
        result = []
        for skill in original_skills:
            if skill.lower().strip() in normalized_skills:
                result.append(skill)
        return result

    def _match_experience(self, resume: Resume, job: Job) -> Optional[str]:
        """
        Check if resume meets experience requirement.

        Args:
            resume: Resume object.
            job: Job object with min_experience_years.

        Returns:
            Description of experience match or None.
        """
        if job.min_experience_years is None:
            return None

        # Estimate years from number of experience entries
        # (Simple heuristic - could be improved with date parsing)
        num_positions = len(resume.experience)
        estimated_years = num_positions * 2  # Rough estimate

        if estimated_years >= job.min_experience_years:
            return f"Experience appears sufficient ({num_positions} positions)"
        else:
            return (
                f"May need more experience "
                f"(has {num_positions} positions, requires {job.min_experience_years}+ years)"
            )

    def _match_education(self, resume: Resume, job: Job) -> Optional[str]:
        """
        Check if resume meets education requirement.

        Args:
            resume: Resume object.
            job: Job object with education_requirements.

        Returns:
            Description of education match or None.
        """
        if not job.education_requirements:
            return None

        if resume.education:
            degrees = [e.degree for e in resume.education if e.degree]
            if degrees:
                return f"Has education: {', '.join(degrees[:2])}"
            return f"Has {len(resume.education)} education entries"
        else:
            return "No education information found"


def calculate_match(
    resume: Resume,
    job: Job,
    resume_embedding: Optional[List[float]] = None,
    job_embedding: Optional[List[float]] = None,
) -> MatchResult:
    """
    Convenience function to calculate match between resume and job.

    Args:
        resume: Resume object.
        job: Job object.
        resume_embedding: Optional pre-computed embedding.
        job_embedding: Optional pre-computed embedding.

    Returns:
        MatchResult with scores and explainability.
    """
    matcher = HybridMatcher()
    return matcher.match(resume, job, resume_embedding, job_embedding)


def rank_resumes_for_job(
    job: Job,
    resumes: List[Resume],
    top_k: int = 10,
) -> List[tuple[Resume, MatchResult]]:
    """
    Rank resumes for a job by match score.

    Args:
        job: Job to match against.
        resumes: List of resumes to rank.
        top_k: Number of top results to return.

    Returns:
        List of (resume, match_result) tuples sorted by score.
    """
    matcher = HybridMatcher()
    job_embedding = matcher.embedding_service.encode(job.raw_text)

    results = []
    for resume in resumes:
        result = matcher.match(resume, job, job_embedding=job_embedding)
        results.append((resume, result))

    # Sort by final score descending
    results.sort(key=lambda x: x[1].final_score, reverse=True)

    return results[:top_k]
