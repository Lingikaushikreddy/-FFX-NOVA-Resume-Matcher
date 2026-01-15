"""
Job posting management endpoints.

Provides API endpoints for creating, retrieving, and
managing job postings.
"""

from fastapi import APIRouter, HTTPException
import logging

from api.schemas import (
    JobCreateRequest,
    JobCreateResponse,
    JobGetResponse,
    JobListResponse,
    JobListItem,
)
from job_parser import parse_job_text
from database import get_db_session, JobDBService
from embeddings import get_embedding_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/create", response_model=JobCreateResponse)
async def create_job(request: JobCreateRequest):
    """
    Create a new job posting.

    Parses the job description to extract skills and requirements,
    generates embedding for semantic matching.

    Returns:
        Job ID and creation confirmation.
    """
    try:
        # Parse job description
        job = parse_job_text(
            text=request.raw_text,
            title=request.title,
            company=request.company,
            location=request.location,
        )

        # Override with provided skills if any
        if request.required_skills is not None:
            job.required_skills = request.required_skills
        if request.preferred_skills is not None:
            job.preferred_skills = request.preferred_skills

        # Generate embedding
        embedding_service = get_embedding_service()
        embedding = embedding_service.encode(job.raw_text)

        # Store in database
        with get_db_session() as session:
            db_job = JobDBService.create(session, job, embedding)

            return JobCreateResponse(
                job_id=db_job.id,
                message="Job created successfully",
                title=job.title,
                company=job.company,
                required_skills_count=len(job.required_skills),
                preferred_skills_count=len(job.preferred_skills),
            )

    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}", response_model=JobGetResponse)
async def get_job(job_id: str):
    """
    Get a job by ID.

    Returns:
        Job data and metadata.
    """
    try:
        with get_db_session() as session:
            db_job = JobDBService.get_by_id(session, job_id)
            if not db_job:
                raise HTTPException(status_code=404, detail="Job not found")

            return JobGetResponse(
                job_id=db_job.id,
                title=db_job.title,
                company=db_job.company,
                location=db_job.location,
                job_data=db_job.job_json,
                created_at=db_job.created_at,
                is_active=bool(db_job.is_active),
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=JobListResponse)
async def list_jobs(limit: int = 100, active_only: bool = True):
    """
    List jobs with optional filtering.

    Args:
        limit: Maximum number of jobs to return.
        active_only: If True, only return active jobs.

    Returns:
        List of job summaries.
    """
    try:
        with get_db_session() as session:
            if active_only:
                jobs = JobDBService.get_active_jobs(session, limit=limit)
            else:
                jobs = session.query(JobDB).limit(limit).all()

            return JobListResponse(
                count=len(jobs),
                jobs=[
                    JobListItem(
                        job_id=j.id,
                        title=j.title,
                        company=j.company,
                        location=j.location,
                    )
                    for j in jobs
                ],
            )

    except Exception as e:
        logger.error(f"Error listing jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{job_id}/deactivate")
async def deactivate_job(job_id: str):
    """
    Deactivate a job posting.

    Returns:
        Confirmation message.
    """
    try:
        with get_db_session() as session:
            success = JobDBService.update_status(session, job_id, is_active=False)
            if not success:
                raise HTTPException(status_code=404, detail="Job not found")

            return {"message": f"Job {job_id} deactivated"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deactivating job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{job_id}/activate")
async def activate_job(job_id: str):
    """
    Activate a job posting.

    Returns:
        Confirmation message.
    """
    try:
        with get_db_session() as session:
            success = JobDBService.update_status(session, job_id, is_active=True)
            if not success:
                raise HTTPException(status_code=404, detail="Job not found")

            return {"message": f"Job {job_id} activated"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activating job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """
    Delete a job by ID.

    Returns:
        Confirmation message.
    """
    try:
        with get_db_session() as session:
            success = JobDBService.delete(session, job_id)
            if not success:
                raise HTTPException(status_code=404, detail="Job not found")

            return {"message": f"Job {job_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/company/{company_name}")
async def get_jobs_by_company(company_name: str):
    """
    Get all jobs for a company.

    Returns:
        List of jobs for the company.
    """
    try:
        with get_db_session() as session:
            jobs = JobDBService.get_by_company(session, company_name)

            return {
                "company": company_name,
                "count": len(jobs),
                "jobs": [
                    {
                        "job_id": j.id,
                        "title": j.title,
                        "location": j.location,
                        "is_active": bool(j.is_active),
                    }
                    for j in jobs
                ],
            }

    except Exception as e:
        logger.error(f"Error getting jobs by company: {e}")
        raise HTTPException(status_code=500, detail=str(e))
