"""
Sentence-transformers embedding service.

Provides text embedding generation with caching support for
efficient semantic similarity calculations.
"""

from functools import lru_cache
from typing import Optional, List
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Lazy loading of sentence-transformers
_model_instance = None


class EmbeddingService:
    """
    Generate embeddings using sentence-transformers.

    Provides methods for encoding text into vector embeddings
    and calculating similarity between embeddings.

    Example:
        service = EmbeddingService()
        embedding = service.encode("Software engineer with Python experience")
        similarity = service.cosine_similarity(embedding1, embedding2)
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        cache_size: int = 1000,
        device: Optional[str] = None,
    ):
        """
        Initialize the embedding service.

        Args:
            model_name: Sentence-transformers model name.
            cache_size: Size of LRU cache for embeddings.
            device: Device to use ('cuda', 'cpu', or None for auto).
        """
        from config import get_settings

        settings = get_settings()
        self.model_name = model_name or settings.embedding_model
        self.cache_size = cache_size
        self.dimension = settings.embedding_dimension
        self.device = device

        self._model = None
        self._encoding_cache = {}

    def _load_model(self):
        """Lazy load the sentence-transformers model."""
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            try:
                from sentence_transformers import SentenceTransformer

                self._model = SentenceTransformer(
                    self.model_name, device=self.device
                )
                logger.info(f"Model loaded successfully: {self.model_name}")
            except ImportError:
                raise ImportError(
                    "sentence-transformers is required for embeddings. "
                    "Install with: pip install sentence-transformers"
                )
        return self._model

    @property
    def model(self):
        """Get the loaded model (lazy loading)."""
        return self._load_model()

    def encode(self, text: str, use_cache: bool = True) -> List[float]:
        """
        Encode text to embedding vector.

        Args:
            text: Text to encode.
            use_cache: Whether to use cached embeddings.

        Returns:
            List of floats representing the embedding.
        """
        if not text or not text.strip():
            # Return zero vector for empty text
            return [0.0] * self.dimension

        text = text.strip()

        # Check cache
        if use_cache and text in self._encoding_cache:
            return self._encoding_cache[text]

        # Generate embedding
        embedding = self.model.encode(text, convert_to_tensor=False)
        result = embedding.tolist()

        # Cache result
        if use_cache:
            if len(self._encoding_cache) >= self.cache_size:
                # Remove oldest entry (simple FIFO)
                oldest_key = next(iter(self._encoding_cache))
                del self._encoding_cache[oldest_key]
            self._encoding_cache[text] = result

        return result

    def encode_batch(
        self, texts: List[str], show_progress: bool = False
    ) -> List[List[float]]:
        """
        Encode multiple texts efficiently.

        Args:
            texts: List of texts to encode.
            show_progress: Whether to show progress bar.

        Returns:
            List of embedding vectors.
        """
        if not texts:
            return []

        # Filter out empty texts and track indices
        non_empty_indices = []
        non_empty_texts = []
        for i, text in enumerate(texts):
            if text and text.strip():
                non_empty_indices.append(i)
                non_empty_texts.append(text.strip())

        if not non_empty_texts:
            return [[0.0] * self.dimension for _ in texts]

        # Encode non-empty texts
        embeddings = self.model.encode(
            non_empty_texts,
            convert_to_tensor=False,
            show_progress_bar=show_progress,
        )

        # Build result list with zero vectors for empty texts
        result = [[0.0] * self.dimension for _ in texts]
        for idx, embedding in zip(non_empty_indices, embeddings):
            result[idx] = embedding.tolist()

        return result

    def cosine_similarity(
        self, embedding1: List[float], embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector.
            embedding2: Second embedding vector.

        Returns:
            Cosine similarity score (0-1 for normalized vectors).
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def find_most_similar(
        self,
        query_embedding: List[float],
        candidate_embeddings: List[List[float]],
        top_k: int = 5,
    ) -> List[tuple[int, float]]:
        """
        Find most similar embeddings to query.

        Args:
            query_embedding: Query vector.
            candidate_embeddings: List of candidate vectors.
            top_k: Number of top results to return.

        Returns:
            List of (index, similarity) tuples sorted by similarity.
        """
        if not candidate_embeddings:
            return []

        similarities = []
        for i, candidate in enumerate(candidate_embeddings):
            sim = self.cosine_similarity(query_embedding, candidate)
            similarities.append((i, sim))

        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def clear_cache(self):
        """Clear the embedding cache."""
        self._encoding_cache.clear()
        logger.info("Embedding cache cleared")

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        return {
            "cache_size": len(self._encoding_cache),
            "max_size": self.cache_size,
            "model_loaded": self._model is not None,
        }


# Singleton instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """
    Get singleton embedding service instance.

    Returns:
        EmbeddingService instance.
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


def reset_embedding_service():
    """Reset the singleton instance (useful for testing)."""
    global _embedding_service
    _embedding_service = None
