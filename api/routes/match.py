"""
Matching endpoints.

Provides API endpoints for calculating matches between
resumes and jobs with explainability.
"""

from fastapi import APIRouter, HTTPException
import logging

from api.schemas import (
    MatchRequest,
    MatchResponse,
    ExplainabilitySchema,
    TopMatchesRequest,
    TopMatchesResponse,
    ResumeMatchesRequest,
    ResumeMatchesResponse,
)
from database import get_db_session, ResumeDBService, JobDBService, MatchDBService
from matching_engine import HybridMatcher
from resume_parser.models.resume import Resume, ContactInfo, WorkExperience, Education
from models.job import Job

logger = logging.getLogger(__name__)
router = APIRouter()


def _build_resume_from_json(resume_json: dict) -> Resume:
    """Build Resume object from stored JSON."""
    contact_data = resume_json.get("contact", {})
    contact = ContactInfo(
        name=contact_data.get("name"),
        email=contact_data.get("email"),
        phone=contact_data.get("phone"),
        location=contact_data.get("location"),
        linkedin=contact_data.get("linkedin"),
    )

    experience = []
    for exp_data in resume_json.get("experience", []):
        experience.append(
            WorkExperience(
                company=exp_data.get("company"),
                role=exp_data.get("role"),
                start_date=exp_data.get("start_date"),
                end_date=exp_data.get("end_date"),
                description=exp_data.get("description"),
                is_current=exp_data.get("is_current", False),
            )
        )

    education = []
    for edu_data in resume_json.get("education", []):
        education.append(
            Education(
                institution=edu_data.get("institution"),
                degree=edu_data.get("degree"),
                field_of_study=edu_data.get("field_of_study"),
                graduation_date=edu_data.get("graduation_date"),
                gpa=edu_data.get("gpa"),
            )
        )

    return Resume(
        raw_text=resume_json.get("raw_text", ""),
        contact=contact,
        skills=resume_json.get("skills", []),
        experience=experience,
        education=education,
    )


def _build_job_from_json(job_json: dict) -> Job:
    """Build Job object from stored JSON."""
    return Job(
        raw_text=job_json.get("raw_text", ""),
        title=job_json.get("title", ""),
        company=job_json.get("company", ""),
        location=job_json.get("location"),
        required_skills=job_json.get("required_skills", []),
        preferred_skills=job_json.get("preferred_skills", []),
        min_experience_years=job_json.get("min_experience_years"),
        education_requirements=job_json.get("education_requirements", []),
    )


def _build_match_response(
    match_result,
    resume_id: str,
    job_id: str,
    match_id: str = None,
) -> MatchResponse:
    """Build MatchResponse from MatchResult."""
    explainability = match_result.explainability

    return MatchResponse(
        match_id=match_id,
        resume_id=resume_id,
        job_id=job_id,
        final_score=match_result.final_score,
        semantic_score=match_result.semantic_score,
        skill_score=match_result.skill_score,
        match_tier=match_result.get_match_tier(),
        explainability=ExplainabilitySchema(
            matched_skills=explainability.matched_skills,
            missing_required_skills=explainability.missing_required_skills,
            missing_preferred_skills=explainability.missing_preferred_skills,
            skill_match_percentage=explainability.skill_match_percentage,
            semantic_similarity=explainability.semantic_similarity,
            experience_match=explainability.experience_match,
            education_match=explainability.education_match,
            explanation_text=explainability.explanation_text,
        ),
    )


@router.post("/", response_model=MatchResponse)
async def calculate_match(request: MatchRequest):
    """
    Calculate match score between a resume and a job.

    Returns detailed match result with explainability.
    The match is stored for future retrieval.

    Returns:
        Match scores and explanation.
    """
    try:
        with get_db_session() as session:
            # Fetch resume and job
            db_resume = ResumeDBService.get_by_id(session, request.resume_id)
            db_job = JobDBService.get_by_id(session, request.job_id)

            if not db_resume:
                raise HTTPException(status_code=404, detail="Resume not found")
            if not db_job:
                raise HTTPException(status_code=404, detail="Job not found")

            # Check for existing match
            existing = MatchDBService.get_existing_match(
                session, request.resume_id, request.job_id
            )
            if existing:
                # Return existing match
                return MatchResponse(
                    match_id=existing.id,
                    resume_id=request.resume_id,
                    job_id=request.job_id,
                    final_score=existing.final_score,
                    semantic_score=existing.semantic_score,
                    skill_score=existing.skill_score,
                    match_tier=_get_tier(existing.final_score),
                    explainability=ExplainabilitySchema(
                        **existing.explainability_json
                    ),
                )

            # Reconstruct objects
            resume = _build_resume_from_json(db_resume.resume_json)
            job = _build_job_from_json(db_job.job_json)

            # Calculate match using pre-computed embeddings
            matcher = HybridMatcher()
            match_result = matcher.match(
                resume=resume,
                job=job,
                resume_embedding=list(db_resume.embedding),
                job_embedding=list(db_job.embedding),
            )

            # Store result
            match_result.resume_id = request.resume_id
            match_result.job_id = request.job_id
            db_match = MatchDBService.create(session, match_result)

            return _build_match_response(
                match_result,
                request.resume_id,
                request.job_id,
                db_match.id,
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating match: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/top-matches", response_model=TopMatchesResponse)
async def get_top_matches_for_job(request: TopMatchesRequest):
    """
    Get top matching resumes for a job.

    Returns pre-calculated matches sorted by score.
    If matches don't exist, calculates them on-the-fly.

    Returns:
        List of top matches for the job.
    """
    try:
        with get_db_session() as session:
            # Verify job exists
            db_job = JobDBService.get_by_id(session, request.job_id)
            if not db_job:
                raise HTTPException(status_code=404, detail="Job not found")

            # Get existing matches
            matches = MatchDBService.get_top_matches_for_job(
                session, request.job_id, request.limit
            )

            match_responses = []
            for m in matches:
                match_responses.append(
                    MatchResponse(
                        match_id=m.id,
                        resume_id=m.resume_id,
                        job_id=m.job_id,
                        final_score=m.final_score,
                        semantic_score=m.semantic_score,
                        skill_score=m.skill_score,
                        match_tier=_get_tier(m.final_score),
                        explainability=ExplainabilitySchema(
                            **m.explainability_json
                        ),
                    )
                )

            return TopMatchesResponse(
                job_id=request.job_id,
                total_matches=len(match_responses),
                matches=match_responses,
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting top matches: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resume-matches", response_model=ResumeMatchesResponse)
async def get_matches_for_resume(request: ResumeMatchesRequest):
    """
    Get top matching jobs for a resume.

    Returns pre-calculated matches sorted by score.

    Returns:
        List of top job matches for the resume.
    """
    try:
        with get_db_session() as session:
            # Verify resume exists
            db_resume = ResumeDBService.get_by_id(session, request.resume_id)
            if not db_resume:
                raise HTTPException(status_code=404, detail="Resume not found")

            # Get existing matches
            matches = MatchDBService.get_matches_for_resume(
                session, request.resume_id, request.limit
            )

            match_responses = []
            for m in matches:
                match_responses.append(
                    MatchResponse(
                        match_id=m.id,
                        resume_id=m.resume_id,
                        job_id=m.job_id,
                        final_score=m.final_score,
                        semantic_score=m.semantic_score,
                        skill_score=m.skill_score,
                        match_tier=_get_tier(m.final_score),
                        explainability=ExplainabilitySchema(
                            **m.explainability_json
                        ),
                    )
                )

            return ResumeMatchesResponse(
                resume_id=request.resume_id,
                total_matches=len(match_responses),
                matches=match_responses,
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting resume matches: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calculate-all-for-job/{job_id}")
async def calculate_all_matches_for_job(job_id: str, limit: int = 100):
    """
    Calculate matches for all resumes against a job.

    Use this to populate matches for a new job.

    Returns:
        Summary of matches calculated.
    """
    try:
        with get_db_session() as session:
            # Get job
            db_job = JobDBService.get_by_id(session, job_id)
            if not db_job:
                raise HTTPException(status_code=404, detail="Job not found")

            job = _build_job_from_json(db_job.job_json)

            # Get all resumes
            resumes = ResumeDBService.get_all(session, limit=limit)

            matcher = HybridMatcher()
            matches_created = 0

            for db_resume in resumes:
                # Skip if match already exists
                existing = MatchDBService.get_existing_match(
                    session, db_resume.id, job_id
                )
                if existing:
                    continue

                resume = _build_resume_from_json(db_resume.resume_json)

                match_result = matcher.match(
                    resume=resume,
                    job=job,
                    resume_embedding=list(db_resume.embedding),
                    job_embedding=list(db_job.embedding),
                )

                match_result.resume_id = db_resume.id
                match_result.job_id = job_id
                MatchDBService.create(session, match_result)
                matches_created += 1

            return {
                "job_id": job_id,
                "matches_created": matches_created,
                "total_resumes_processed": len(resumes),
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating all matches: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _get_tier(score: float) -> str:
    """Get match quality tier from score."""
    if score >= 0.85:
        return "Excellent"
    elif score >= 0.70:
        return "Strong"
    elif score >= 0.55:
        return "Good"
    elif score >= 0.40:
        return "Fair"
    else:
        return "Weak"
