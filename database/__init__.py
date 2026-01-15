"""
Database module for FFX NOVA Resume Matcher.

Provides connection management and CRUD operations for
PostgreSQL with pgvector.
"""

from database.connection import (
    get_db_engine,
    get_db_session,
    init_db,
    SessionLocal,
)
from database.crud import ResumeDBService, JobDBService, MatchDBService

__all__ = [
    "get_db_engine",
    "get_db_session",
    "init_db",
    "SessionLocal",
    "ResumeDBService",
    "JobDBService",
    "MatchDBService",
]
