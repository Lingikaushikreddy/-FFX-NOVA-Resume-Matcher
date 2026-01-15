#!/usr/bin/env python3
"""
Main application entry point.

Starts the FastAPI server using uvicorn.
"""

import uvicorn
from config import get_settings


def main():
    """Run the API server."""
    settings = get_settings()

    print("=" * 60)
    print("FFX NOVA Resume Matcher API")
    print("=" * 60)
    print(f"Version: {settings.api_version}")
    print(f"Host: {settings.api_host}")
    print(f"Port: {settings.api_port}")
    print(f"Docs: http://{settings.api_host}:{settings.api_port}/docs")
    print("=" * 60)

    uvicorn.run(
        "api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
        log_level="info",
    )


if __name__ == "__main__":
    main()
