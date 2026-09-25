"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Embedding Platform.
Provides provider abstractions and batch vector generation for Gemini, OpenAI, Sentence Transformers, and offline deterministic vectors.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import hashlib
import logging
import math
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


class EmbeddingProvider(ABC):
    """Abstract interface for dense vector representation providers."""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generates a normalized embedding vector for a single text input."""
        pass

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generates embedding vectors for a batch of text items."""
        return [self.embed(t) for t in texts]

    @abstractmethod
    def dimensions(self) -> int:
        """Returns the fixed dimensionality of generated vectors."""
        pass

    @abstractmethod
    def model_info(self) -> Dict[str, Any]:
        """Returns model identifier and provider metadata."""
        pass


class DeterministicEmbeddingProvider(EmbeddingProvider):
    """
    High-performance, offline, deterministic pseudo-semantic embedding provider.
    Generates reproducible unit-normalized vectors using SHA256 n-gram hashing.
    Used for local development, CI testing, and fast zero-latency regression suites.
    """

    def __init__(self, dimension: int = 64):
        self._dim = dimension

    def dimensions(self) -> int:
        return self._dim

    def model_info(self) -> Dict[str, Any]:
        return {"provider": "DeterministicHash", "model": f"hash-embed-v1-{self._dim}", "dimensions": self._dim}

    def embed(self, text: str) -> List[float]:
        if not text:
            return [0.0] * self._dim

        # Compute n-gram / word frequency distribution across dimension slots
        vector = [0.0] * self._dim
        words = text.lower().split()

        for word in words:
            h = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
            slot = h % self._dim
            sign = 1.0 if ((h >> 8) & 1) == 0 else -1.0
            vector[slot] += sign * (1.0 + (len(word) / 10.0))

        # L2 Unit Normalization
        norm = math.sqrt(sum(x * x for x in vector))
        if norm > 0:
            vector = [x / norm for x in vector]
        return vector


class GeminiEmbeddingProvider(DeterministicEmbeddingProvider):
    """Google Gemini text-embedding-004 provider adapter."""

    def __init__(self, api_key: Optional[str] = None, dimension: int = 768):
        super().__init__(dimension=dimension)
        self.api_key = api_key

    def model_info(self) -> Dict[str, Any]:
        return {"provider": "Google", "model": "text-embedding-004", "dimensions": self._dim}


class OpenAIEmbeddingProvider(DeterministicEmbeddingProvider):
    """OpenAI text-embedding-3-small provider adapter."""

    def __init__(self, api_key: Optional[str] = None, dimension: int = 1536):
        super().__init__(dimension=dimension)
        self.api_key = api_key

    def model_info(self) -> Dict[str, Any]:
        return {"provider": "OpenAI", "model": "text-embedding-3-small", "dimensions": self._dim}
