"""
Resume upload and management endpoints.

Provides API endpoints for uploading, retrieving, and
managing resumes in the system.
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
import logging
import tempfile
import os
import shutil

from api.schemas import (
    ResumeUploadRequest,
    ResumeUploadResponse,
    ResumeGetResponse,
)
from resume_parser.models.resume import Resume, ContactInfo
from resume_parser.parser import ResumeParser
from database import get_db_session, ResumeDBService
from embeddings import get_embedding_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(request: ResumeUploadRequest):
    """
    Upload a parsed resume and store it in the database.

    Expects resume_json from resume_parser.parse() output.
    Generates embedding for semantic matching.

    Returns:
        Resume ID and upload confirmation.
    """
    try:
        resume_data = request.resume_json

        # Build Resume object from JSON
        contact_data = resume_data.get("contact", {})
        contact = ContactInfo(
            name=contact_data.get("name"),
            email=contact_data.get("email"),
            phone=contact_data.get("phone"),
            location=contact_data.get("location"),
            linkedin=contact_data.get("linkedin"),
        )

        resume = Resume(
            raw_text=resume_data.get("raw_text", ""),
            contact=contact,
            skills=resume_data.get("skills", []),
            file_path=resume_data.get("file_path"),
            file_type=resume_data.get("file_type"),
        )

        # Generate embedding
        embedding_service = get_embedding_service()
        embedding = embedding_service.encode(resume.raw_text)

        # Store in database
        with get_db_session() as session:
            # Check for existing resume by email
            if resume.contact.email:
                existing = ResumeDBService.get_by_email(
                    session, resume.contact.email
                )
                if existing:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Resume already exists for email: {resume.contact.email}",
                    )

            db_resume = ResumeDBService.create(
                session, resume, embedding, file_path=resume.file_path
            )

            return ResumeUploadResponse(
                resume_id=db_resume.id,
                message="Resume uploaded successfully",
                candidate_name=resume.contact.name,
                candidate_email=resume.contact.email,
                skills_count=len(resume.skills),
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-file", response_model=ResumeUploadResponse)
async def upload_resume_file(file: UploadFile = File(...)):
    """
    Upload a resume file (PDF/DOCX), parse it, and store in database.
    """
    tmp_path = None
    try:
        # Validate file type
        filename = file.filename or "unknown"
        if not filename.lower().endswith(('.pdf', '.docx')):
             raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

        # Save to temp file
        suffix = os.path.splitext(filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # Parse resume
        parser = ResumeParser()
        resume = parser.parse(tmp_path)
        
        # Add file metadata
        resume.file_path = filename # Store original filename
        resume.file_type = suffix[1:] if suffix else "" # pdf or docx
        
        # Generate embedding
        embedding_service = get_embedding_service()
        embedding = embedding_service.encode(resume.raw_text)

        # Store in database
        with get_db_session() as session:
            # Check for existing by email if present
            # Note: For now we allow re-uploads or handle duplicates gracefully
            if resume.contact.email:
                existing = ResumeDBService.get_by_email(session, resume.contact.email)
                if existing:
                     # Update or just log? For simple demo, we can just return the existing one or overwrite
                     pass 

            db_resume = ResumeDBService.create(
                session, resume, embedding, file_path=filename
            )

            return ResumeUploadResponse(
                resume_id=db_resume.id,
                message="Resume processed successfully",
                candidate_name=resume.contact.name,
                candidate_email=resume.contact.email,
                skills_count=len(resume.skills)
            )

    except Exception as e:
        logger.error(f"Error processing file upload: {e}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    finally:
        # Cleanup temp file
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.get("/{resume_id}", response_model=ResumeGetResponse)
async def get_resume(resume_id: str):
    """
    Get a resume by ID.

    Returns:
        Resume data and metadata.
    """
    try:
        with get_db_session() as session:
            db_resume = ResumeDBService.get_by_id(session, resume_id)
            if not db_resume:
                raise HTTPException(status_code=404, detail="Resume not found")

            return ResumeGetResponse(
                resume_id=db_resume.id,
                resume_data=db_resume.resume_json,
                created_at=db_resume.created_at,
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_resumes(limit: int = 100, offset: int = 0):
    """
    List all resumes with pagination.

    Returns:
        List of resume summaries.
    """
    try:
        with get_db_session() as session:
            resumes = ResumeDBService.get_all(session, limit=limit, offset=offset)
            total = ResumeDBService.count(session)

            return {
                "total": total,
                "count": len(resumes),
                "offset": offset,
                "resumes": [
                    {
                        "resume_id": r.id,
                        "candidate_name": r.candidate_name,
                        "candidate_email": r.candidate_email,
                        "skills_count": len(r.skills) if r.skills else 0,
                        "created_at": r.created_at,
                    }
                    for r in resumes
                ],
            }

    except Exception as e:
        logger.error(f"Error listing resumes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{resume_id}")
async def delete_resume(resume_id: str):
    """
    Delete a resume by ID.

    Returns:
        Confirmation message.
    """
    try:
        with get_db_session() as session:
            success = ResumeDBService.delete(session, resume_id)
            if not success:
                raise HTTPException(status_code=404, detail="Resume not found")

            return {"message": f"Resume {resume_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/by-skills")
async def search_by_skills(skills: str, limit: int = 10):
    """
    Search resumes by skills.

    Args:
        skills: Comma-separated list of skills.
        limit: Maximum results.

    Returns:
        List of matching resumes.
    """
    try:
        skill_list = [s.strip() for s in skills.split(",") if s.strip()]
        if not skill_list:
            raise HTTPException(
                status_code=400, detail="At least one skill required"
            )

        with get_db_session() as session:
            resumes = ResumeDBService.search_by_skills(
                session, skill_list, limit=limit
            )

            return {
                "search_skills": skill_list,
                "count": len(resumes),
                "resumes": [
                    {
                        "resume_id": r.id,
                        "candidate_name": r.candidate_name,
                        "skills": r.skills,
                    }
                    for r in resumes
                ],
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching resumes: {e}")
        raise HTTPException(status_code=500, detail=str(e))
