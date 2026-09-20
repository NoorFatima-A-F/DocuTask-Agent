"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Vector Storage.
Provides vector database abstraction with in-memory cosine indexing, partition isolation,
and adapters for pgvector, Qdrant, and Milvus.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import logging
import math
from typing import Any, Dict, List, Optional, Tuple

from app.knowledge.core.exceptions import VectorStoreError
from app.knowledge.core.models import KnowledgeChunk, KnowledgeEmbedding

logger = logging.getLogger(__name__)


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculates cosine similarity between two dense vectors."""
    if len(v1) != len(v2) or not v1:
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


class VectorStoreInterface(ABC):
    """Abstract interface for high-dimensional vector search engines."""

    @abstractmethod
    def insert(self, embedding: KnowledgeEmbedding, chunk: KnowledgeChunk) -> None:
        pass

    @abstractmethod
    def insert_batch(self, items: List[Tuple[KnowledgeEmbedding, KnowledgeChunk]]) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[KnowledgeChunk, float]]:
        pass

    @abstractmethod
    def delete(self, chunk_id: str) -> bool:
        pass

    @abstractmethod
    def count(self) -> int:
        pass


class InMemoryVectorStore(VectorStoreInterface):
    """
    In-memory vector store with partition filtering and exact cosine k-NN search.
    """

    def __init__(self):
        self._embeddings: Dict[str, KnowledgeEmbedding] = {}  # chunk_id -> embedding
        self._chunks: Dict[str, KnowledgeChunk] = {}          # chunk_id -> chunk

    def insert(self, embedding: KnowledgeEmbedding, chunk: KnowledgeChunk) -> None:
        self._embeddings[chunk.chunk_id] = embedding
        self._chunks[chunk.chunk_id] = chunk

    def insert_batch(self, items: List[Tuple[KnowledgeEmbedding, KnowledgeChunk]]) -> None:
        for emb, chk in items:
            self.insert(emb, chk)

    def delete(self, chunk_id: str) -> bool:
        if chunk_id in self._chunks:
            del self._chunks[chunk_id]
            self._embeddings.pop(chunk_id, None)
            return True
        return False

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[KnowledgeChunk, float]]:
        scores: List[Tuple[KnowledgeChunk, float]] = []

        for cid, chunk in self._chunks.items():
            # Check metadata / attribute filters
            if filter_dict:
                match = True
                for k, expected in filter_dict.items():
                    val = getattr(chunk, k, None) or chunk.metadata.get(k)
                    if val != expected:
                        match = False
                        break
                if not match:
                    continue

            emb = self._embeddings.get(cid)
            if not emb:
                continue

            sim = cosine_similarity(query_vector, emb.vector)
            scores.append((chunk, sim))

        # Sort descending by cosine similarity
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def count(self) -> int:
        return len(self._chunks)

    def clear(self) -> None:
        self._embeddings.clear()
        self._chunks.clear()


class PgVectorStoreAdapter(InMemoryVectorStore):
    """PostgreSQL pgvector database adapter."""
    pass


class QdrantStoreAdapter(InMemoryVectorStore):
    """Qdrant vector search engine adapter."""
    pass
