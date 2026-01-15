"""
Database connection management.

Provides SQLAlchemy engine, session management, and database
initialization with pgvector extension support.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator, Optional
import logging

from config import get_settings
from models.db_models import Base, VECTOR_INDEXES

logger = logging.getLogger(__name__)

# Session factory (configured lazily)
SessionLocal = sessionmaker(autocommit=False, autoflush=False)

# Cached engine
_engine = None


def get_db_engine(database_url: Optional[str] = None):
    """
    Create or return cached database engine.

    Args:
        database_url: Optional database URL (uses settings if not provided).

    Returns:
        SQLAlchemy Engine instance.
    """
    global _engine

    if _engine is not None and database_url is None:
        return _engine

    settings = get_settings()
    url = database_url or settings.database_url

    logger.info(f"Creating database engine for: {url.split('@')[-1]}")

    engine = create_engine(
        url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        echo=settings.api_debug,
    )

    if database_url is None:
        _engine = engine

    return engine


def init_db(engine=None, create_vector_indexes: bool = True) -> None:
    """
    Initialize database tables and extensions.

    Creates all tables defined in models and optionally
    creates pgvector extension and indexes.

    Args:
        engine: SQLAlchemy engine (uses default if not provided).
        create_vector_indexes: Whether to create vector indexes.
    """
    if engine is None:
        engine = get_db_engine()

    logger.info("Initializing database...")

    # Create pgvector extension
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            logger.info("pgvector extension enabled")
    except Exception as e:
        logger.warning(f"Could not create pgvector extension: {e}")
        logger.warning("Vector similarity search may not be available")

    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

    # Create vector indexes
    if create_vector_indexes:
        try:
            with engine.connect() as conn:
                for statement in VECTOR_INDEXES.split(";"):
                    statement = statement.strip()
                    if statement:
                        conn.execute(text(statement))
                conn.commit()
                logger.info("Vector indexes created")
        except Exception as e:
            logger.warning(f"Could not create vector indexes: {e}")


def drop_all_tables(engine=None) -> None:
    """
    Drop all database tables.

    WARNING: This will delete all data!

    Args:
        engine: SQLAlchemy engine (uses default if not provided).
    """
    if engine is None:
        engine = get_db_engine()

    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("All tables dropped")


@contextmanager
def get_db_session(engine=None) -> Generator[Session, None, None]:
    """
    Context manager for database sessions.

    Handles commit on success and rollback on failure.

    Args:
        engine: SQLAlchemy engine (uses default if not provided).

    Yields:
        SQLAlchemy Session instance.

    Example:
        with get_db_session() as session:
            result = session.query(ResumeDB).all()
    """
    if engine is None:
        engine = get_db_engine()

    SessionLocal.configure(bind=engine)
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def get_session_dependency(engine=None) -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.

    Use with FastAPI's Depends() for automatic session management.

    Yields:
        SQLAlchemy Session instance.
    """
    if engine is None:
        engine = get_db_engine()

    SessionLocal.configure(bind=engine)
    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
