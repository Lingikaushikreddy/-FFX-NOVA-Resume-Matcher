"""
Semantic similarity scorer using sentence-transformers.

Calculates cosine similarity between resume and job embeddings
for semantic/conceptual matching.
"""

from typing import List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class SemanticScorer:
    """
    Semantic similarity scorer using sentence-transformers.

    Uses the existing EmbeddingService from the embeddings module
    for efficient, cached embedding generation.

    Example:
        >>> scorer = SemanticScorer()
        >>> score = scorer.score(resume_text, job_text)
        >>> print(f"Semantic similarity: {score:.2f}")
    """

    def __init__(self):
        """Initialize semantic scorer with embedding service."""
        self._embedding_service = None

    @property
    def embedding_service(self):
        """Lazy-load embedding service."""
        if self._embedding_service is None:
            try:
                from embeddings import get_embedding_service
                self._embedding_service = get_embedding_service()
            except ImportError:
                logger.warning(
                    "Embeddings module not available, using fallback scorer"
                )
                self._embedding_service = FallbackEmbeddingService()
        return self._embedding_service

    def score(
        self,
        resume_text: str,
        job_text: str,
        resume_embedding: Optional[List[float]] = None,
        job_embedding: Optional[List[float]] = None,
    ) -> float:
        """
        Calculate semantic similarity between resume and job.

        Args:
            resume_text: Resume raw text.
            job_text: Job description text.
            resume_embedding: Pre-computed resume embedding (optional).
            job_embedding: Pre-computed job embedding (optional).

        Returns:
            Cosine similarity score between 0 and 1.
        """
        if not resume_text or not job_text:
            return 0.0

        # Generate embeddings if not provided
        if resume_embedding is None:
            resume_embedding = self.embedding_service.encode(resume_text)
        if job_embedding is None:
            job_embedding = self.embedding_service.encode(job_text)

        # Calculate cosine similarity
        similarity = self.embedding_service.cosine_similarity(
            resume_embedding, job_embedding
        )

        # Ensure in valid range
        return max(0.0, min(1.0, similarity))

    def score_batch(
        self,
        resume_text: str,
        job_texts: List[str],
        resume_embedding: Optional[List[float]] = None,
    ) -> List[float]:
        """
        Calculate semantic similarity for multiple jobs efficiently.

        Args:
            resume_text: Resume raw text.
            job_texts: List of job description texts.
            resume_embedding: Pre-computed resume embedding (optional).

        Returns:
            List of similarity scores.
        """
        if not resume_text or not job_texts:
            return []

        # Generate resume embedding once
        if resume_embedding is None:
            resume_embedding = self.embedding_service.encode(resume_text)

        # Generate job embeddings in batch
        job_embeddings = self.embedding_service.encode_batch(job_texts)

        # Calculate similarities
        scores = []
        for job_emb in job_embeddings:
            similarity = self.embedding_service.cosine_similarity(
                resume_embedding, job_emb
            )
            scores.append(max(0.0, min(1.0, similarity)))

        return scores


class FallbackEmbeddingService:
    """
    Fallback embedding service when sentence-transformers is unavailable.

    Uses simple TF-IDF based similarity as a fallback.
    """

    def __init__(self):
        """Initialize fallback service."""
        self._vectorizer = None

    @property
    def vectorizer(self):
        """Lazy-load TF-IDF vectorizer."""
        if self._vectorizer is None:
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                self._vectorizer = TfidfVectorizer(
                    max_features=1000,
                    stop_words="english",
                    ngram_range=(1, 2),
                )
            except ImportError:
                logger.error("scikit-learn not available for fallback")
                self._vectorizer = None
        return self._vectorizer

    def encode(self, text: str) -> List[float]:
        """Encode text using TF-IDF (returns sparse representation)."""
        if self.vectorizer is None:
            return [0.0] * 384

        try:
            vector = self.vectorizer.fit_transform([text])
            return vector.toarray()[0].tolist()
        except Exception:
            return [0.0] * 384

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encode multiple texts."""
        return [self.encode(t) for t in texts]

    def cosine_similarity(
        self,
        embedding1: Union[List[float], any],
        embedding2: Union[List[float], any],
    ) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            import numpy as np

            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)

            # Handle dimension mismatch
            if vec1.shape != vec2.shape:
                min_len = min(len(vec1), len(vec2))
                vec1 = vec1[:min_len]
                vec2 = vec2[:min_len]

            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)

            if norm1 == 0 or norm2 == 0:
                return 0.0

            return float(dot_product / (norm1 * norm2))
        except Exception:
            return 0.5  # Default fallback
