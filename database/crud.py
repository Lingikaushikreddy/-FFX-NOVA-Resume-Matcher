"""
CRUD operations for database entities.

Provides service classes for creating, reading, updating, and
deleting resumes, jobs, and match results.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from dataclasses import asdict
import logging

from models.db_models import ResumeDB, JobDB, MatchResultDB
from resume_parser.models.resume import Resume
from models.job import Job
from models.match_result import MatchResult

logger = logging.getLogger(__name__)


class ResumeDBService:
    """CRUD operations for resumes."""

    @staticmethod
    def create(
        session: Session,
        resume: Resume,
        embedding: list[float],
        file_path: Optional[str] = None,
    ) -> ResumeDB:
        """
        Create a new resume record with embedding.

        Args:
            session: Database session.
            resume: Parsed Resume object.
            embedding: Vector embedding for semantic search.
            file_path: Optional path to original file.

        Returns:
            Created ResumeDB instance.
        """
        db_resume = ResumeDB(
            resume_json=resume.to_dict(),
            raw_text=resume.raw_text,
            candidate_name=resume.contact.name,
            candidate_email=resume.contact.email,
            skills=resume.skills,
            embedding=embedding,
            file_path=file_path,
        )
        session.add(db_resume)
        session.flush()
        logger.info(f"Created resume: {db_resume.id}")
        return db_resume

    @staticmethod
    def get_by_id(session: Session, resume_id: str) -> Optional[ResumeDB]:
        """Get resume by ID."""
        return session.query(ResumeDB).filter(ResumeDB.id == resume_id).first()

    @staticmethod
    def get_by_email(session: Session, email: str) -> Optional[ResumeDB]:
        """Get resume by candidate email."""
        return (
            session.query(ResumeDB)
            .filter(ResumeDB.candidate_email == email)
            .first()
        )

    @staticmethod
    def get_all(session: Session, limit: int = 100, offset: int = 0) -> List[ResumeDB]:
        """Get all resumes with pagination."""
        return (
            session.query(ResumeDB)
            .order_by(desc(ResumeDB.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def search_by_skills(
        session: Session, skills: list[str], limit: int = 10
    ) -> List[ResumeDB]:
        """
        Search resumes that contain any of the given skills.

        Args:
            session: Database session.
            skills: List of skills to search for.
            limit: Maximum results to return.

        Returns:
            List of matching ResumeDB instances.
        """
        # Use PostgreSQL JSONB contains operator
        results = []
        for resume in session.query(ResumeDB).limit(limit * 2).all():
            if resume.skills:
                resume_skills_lower = [s.lower() for s in resume.skills]
                search_skills_lower = [s.lower() for s in skills]
                if any(s in resume_skills_lower for s in search_skills_lower):
                    results.append(resume)
                    if len(results) >= limit:
                        break
        return results

    @staticmethod
    def delete(session: Session, resume_id: str) -> bool:
        """Delete a resume by ID."""
        resume = ResumeDBService.get_by_id(session, resume_id)
        if resume:
            session.delete(resume)
            session.flush()
            logger.info(f"Deleted resume: {resume_id}")
            return True
        return False

    @staticmethod
    def count(session: Session) -> int:
        """Get total count of resumes."""
        return session.query(ResumeDB).count()


class JobDBService:
    """CRUD operations for jobs."""

    @staticmethod
    def create(session: Session, job: Job, embedding: list[float]) -> JobDB:
        """
        Create a new job record with embedding.

        Args:
            session: Database session.
            job: Parsed Job object.
            embedding: Vector embedding for semantic matching.

        Returns:
            Created JobDB instance.
        """
        db_job = JobDB(
            job_json=job.to_dict(),
            raw_text=job.raw_text,
            title=job.title,
            company=job.company,
            location=job.location,
            required_skills=job.required_skills,
            preferred_skills=job.preferred_skills,
            embedding=embedding,
            is_active=True,
        )
        session.add(db_job)
        session.flush()
        logger.info(f"Created job: {db_job.id} - {job.title}")
        return db_job

    @staticmethod
    def get_by_id(session: Session, job_id: str) -> Optional[JobDB]:
        """Get job by ID."""
        return session.query(JobDB).filter(JobDB.id == job_id).first()

    @staticmethod
    def get_active_jobs(session: Session, limit: int = 100) -> List[JobDB]:
        """Get all active jobs."""
        return (
            session.query(JobDB)
            .filter(JobDB.is_active == True)  # noqa: E712
            .order_by(desc(JobDB.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_company(session: Session, company: str) -> List[JobDB]:
        """Get jobs by company name."""
        return (
            session.query(JobDB)
            .filter(JobDB.company == company)
            .filter(JobDB.is_active == True)  # noqa: E712
            .all()
        )

    @staticmethod
    def update_status(session: Session, job_id: str, is_active: bool) -> bool:
        """Update job active status."""
        job = JobDBService.get_by_id(session, job_id)
        if job:
            job.is_active = is_active
            session.flush()
            logger.info(f"Updated job {job_id} status to {is_active}")
            return True
        return False

    @staticmethod
    def delete(session: Session, job_id: str) -> bool:
        """Delete a job by ID."""
        job = JobDBService.get_by_id(session, job_id)
        if job:
            session.delete(job)
            session.flush()
            logger.info(f"Deleted job: {job_id}")
            return True
        return False

    @staticmethod
    def count(session: Session, active_only: bool = True) -> int:
        """Get total count of jobs."""
        query = session.query(JobDB)
        if active_only:
            query = query.filter(JobDB.is_active == True)  # noqa: E712
        return query.count()


class MatchDBService:
    """CRUD operations for match results."""

    @staticmethod
    def create(session: Session, match_result: MatchResult) -> MatchResultDB:
        """
        Store a match result.

        Args:
            session: Database session.
            match_result: MatchResult object.

        Returns:
            Created MatchResultDB instance.
        """
        explainability_dict = (
            match_result.explainability.to_dict()
            if hasattr(match_result.explainability, "to_dict")
            else asdict(match_result.explainability)
        )

        db_match = MatchResultDB(
            resume_id=match_result.resume_id,
            job_id=match_result.job_id,
            final_score=match_result.final_score,
            semantic_score=match_result.semantic_score,
            skill_score=match_result.skill_score,
            explainability_json=explainability_dict,
        )
        session.add(db_match)
        session.flush()
        logger.info(
            f"Created match: resume={match_result.resume_id}, "
            f"job={match_result.job_id}, score={match_result.final_score:.2f}"
        )
        return db_match

    @staticmethod
    def get_by_id(session: Session, match_id: str) -> Optional[MatchResultDB]:
        """Get match result by ID."""
        return (
            session.query(MatchResultDB)
            .filter(MatchResultDB.id == match_id)
            .first()
        )

    @staticmethod
    def get_existing_match(
        session: Session, resume_id: str, job_id: str
    ) -> Optional[MatchResultDB]:
        """Get existing match between resume and job."""
        return (
            session.query(MatchResultDB)
            .filter(
                and_(
                    MatchResultDB.resume_id == resume_id,
                    MatchResultDB.job_id == job_id,
                )
            )
            .first()
        )

    @staticmethod
    def get_top_matches_for_job(
        session: Session, job_id: str, limit: int = 10
    ) -> List[MatchResultDB]:
        """
        Get top N resume matches for a job.

        Args:
            session: Database session.
            job_id: Job ID to get matches for.
            limit: Maximum number of matches to return.

        Returns:
            List of MatchResultDB ordered by score descending.
        """
        return (
            session.query(MatchResultDB)
            .filter(MatchResultDB.job_id == job_id)
            .order_by(desc(MatchResultDB.final_score))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_matches_for_resume(
        session: Session, resume_id: str, limit: int = 10
    ) -> List[MatchResultDB]:
        """
        Get top N job matches for a resume.

        Args:
            session: Database session.
            resume_id: Resume ID to get matches for.
            limit: Maximum number of matches to return.

        Returns:
            List of MatchResultDB ordered by score descending.
        """
        return (
            session.query(MatchResultDB)
            .filter(MatchResultDB.resume_id == resume_id)
            .order_by(desc(MatchResultDB.final_score))
            .limit(limit)
            .all()
        )

    @staticmethod
    def delete_for_job(session: Session, job_id: str) -> int:
        """Delete all matches for a job."""
        count = (
            session.query(MatchResultDB)
            .filter(MatchResultDB.job_id == job_id)
            .delete()
        )
        session.flush()
        logger.info(f"Deleted {count} matches for job {job_id}")
        return count

    @staticmethod
    def count(session: Session) -> int:
        """Get total count of match results."""
        return session.query(MatchResultDB).count()
