"""
Application settings using Pydantic.

Loads configuration from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """
    Application configuration settings.

    All settings can be overridden via environment variables.
    """

    # Database Configuration
    database_url: str = "postgresql://postgres:password@localhost:5432/resume_matcher"

    # Embedding Model Configuration
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    embedding_cache_size: int = 1000

    # Matching Algorithm Weights
    semantic_weight: float = 0.4
    skill_weight: float = 0.6

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "FFX NOVA Resume Matcher API"
    api_version: str = "1.0.0"
    api_debug: bool = False

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def validate_weights(self) -> bool:
        """Validate that matching weights sum to 1.0."""
        return abs(self.semantic_weight + self.skill_weight - 1.0) < 0.01


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings object with current configuration.
    """
    return Settings()
