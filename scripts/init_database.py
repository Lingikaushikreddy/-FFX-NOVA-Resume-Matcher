#!/usr/bin/env python3
"""
Initialize database with pgvector extension and tables.

Run this script to set up the database before starting the API.
"""

import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Initialize the database."""
    print("=" * 60)
    print("FFX NOVA Resume Matcher - Database Initialization")
    print("=" * 60)

    try:
        from config import get_settings

        settings = get_settings()
        print(f"Database URL: {settings.database_url.split('@')[-1]}")
        print()

        from database import init_db, get_db_engine

        engine = get_db_engine()
        print("Connecting to database...")

        init_db(engine, create_vector_indexes=True)

        print()
        print("=" * 60)
        print("Database initialized successfully!")
        print("=" * 60)
        print()
        print("Tables created:")
        print("  - resumes")
        print("  - jobs")
        print("  - match_results")
        print()
        print("You can now start the API with: python main.py")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        print()
        print("=" * 60)
        print("ERROR: Database initialization failed!")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Make sure:")
        print("  1. PostgreSQL is running")
        print("  2. pgvector extension is installed")
        print("  3. Database connection URL is correct in .env")
        print()
        print("To install pgvector with Docker:")
        print("  docker run -d --name pgvector \\")
        print("    -e POSTGRES_PASSWORD=password \\")
        print("    -p 5432:5432 \\")
        print("    pgvector/pgvector:pg16")
        sys.exit(1)


if __name__ == "__main__":
    main()
