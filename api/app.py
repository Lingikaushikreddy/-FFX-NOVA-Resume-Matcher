"""
FastAPI application setup.

Main application entry point with route registration
and middleware configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="""
    FFX NOVA Resume Matcher API

    AI-powered resume and job matching system using hybrid
    semantic-keyword matching for explainable, high-accuracy results.

    ## Features

    - **Resume Upload**: Parse and store resumes with vector embeddings
    - **Job Creation**: Create job postings with skill extraction
    - **Matching**: Calculate match scores with detailed explainability
    - **Ranking**: Get top matches for jobs or resumes

    ## Matching Algorithm

    Uses a weighted combination of:
    - **Semantic Similarity (40%)**: Cosine similarity of text embeddings
    - **Skill Matching (60%)**: Exact skill overlap (required skills weighted 2x)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from api.routes import resume, job, match

app.include_router(resume.router, prefix="/api/v1/resumes", tags=["Resumes"])
app.include_router(job.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(match.router, prefix="/api/v1/match", tags=["Matching"])


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "FFX NOVA Resume Matcher API",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns service status and component availability.
    """
    health_status = {
        "status": "healthy",
        "version": settings.api_version,
        "database_connected": False,
        "embedding_model_loaded": False,
    }

    # Check database connection
    try:
        from database import get_db_session

        with get_db_session() as session:
            session.execute("SELECT 1")
            health_status["database_connected"] = True
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")

    # Check embedding service
    try:
        from embeddings import get_embedding_service

        service = get_embedding_service()
        stats = service.get_cache_stats()
        health_status["embedding_model_loaded"] = stats.get("model_loaded", False)
    except Exception as e:
        logger.warning(f"Embedding service health check failed: {e}")

    return health_status


@app.get("/stats", tags=["Health"])
async def get_stats():
    """
    Get system statistics.

    Returns counts of resumes, jobs, and matches.
    """
    try:
        from database import get_db_session, ResumeDBService, JobDBService, MatchDBService

        with get_db_session() as session:
            return {
                "total_resumes": ResumeDBService.count(session),
                "total_jobs": JobDBService.count(session, active_only=False),
                "active_jobs": JobDBService.count(session, active_only=True),
                "total_matches": MatchDBService.count(session),
            }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {
            "error": str(e),
            "total_resumes": 0,
            "total_jobs": 0,
            "active_jobs": 0,
            "total_matches": 0,
        }


@app.on_event("startup")
async def startup_event():
    """
    Application startup event.

    Pre-loads embedding model for faster first request.
    """
    logger.info("Starting FFX NOVA Resume Matcher API [Environment: Production]")
    logger.info(f"API Version: {settings.api_version}")
    logger.info(f"Semantic Weight: {settings.semantic_weight}")
    logger.info(f"Skill Weight: {settings.skill_weight}")

    # Optionally pre-load embedding model
    # Uncomment to load model at startup (slower startup but faster first request)
    # try:
    #     from embeddings import get_embedding_service
    #     service = get_embedding_service()
    #     service.encode("warm up")
    #     logger.info("Embedding model pre-loaded")
    # except Exception as e:
    #     logger.warning(f"Could not pre-load embedding model: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.
    """
    logger.info("Shutting down FFX NOVA Resume Matcher API...")
