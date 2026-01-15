"""
Embedding service module for FFX NOVA Resume Matcher.

Provides sentence-transformers integration for generating
vector embeddings.
"""

from embeddings.service import EmbeddingService, get_embedding_service

__all__ = ["EmbeddingService", "get_embedding_service"]
