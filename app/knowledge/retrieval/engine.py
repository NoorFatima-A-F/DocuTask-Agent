"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Hybrid Retrieval Engine.
Combines BM25 lexical keyword matching, dense vector semantic similarity, metadata filtering,
and Reciprocal Rank Fusion (RRF).
"""

from __future__ import annotations

import logging
import math
from typing import Any, Dict, List, Optional, Tuple

from app.knowledge.core.models import KnowledgeChunk, KnowledgeEmbedding, RetrievalResult
from app.knowledge.embeddings.provider import DeterministicEmbeddingProvider, EmbeddingProvider
from app.knowledge.vector.store import InMemoryVectorStore, VectorStoreInterface

logger = logging.getLogger(__name__)


def bm25_score(query_tokens: List[str], doc_tokens: List[str], k1: float = 1.5, b: float = 0.75, avgdl: float = 100.0) -> float:
    """Calculates standard BM25 score for a document against query tokens."""
    if not query_tokens or not doc_tokens:
        return 0.0

    dl = len(doc_tokens)
    doc_term_freq: Dict[str, int] = {}
    for t in doc_tokens:
        doc_term_freq[t] = doc_term_freq.get(t, 0) + 1

    score = 0.0
    for q in query_tokens:
        if q in doc_term_freq:
            tf = doc_term_freq[q]
            # IDF approximation
            idf = math.log(1.0 + (100.0 / (1.0 + tf)))
            num = tf * (k1 + 1.0)
            denom = tf + k1 * (1.0 - b + b * (dl / max(1.0, avgdl)))
            score += idf * (num / max(0.0001, denom))

    return score


class HybridRetrievalEngine:
    """
    Enterprise hybrid retrieval platform fusing lexical BM25 and dense semantic search.
    """

    def __init__(
        self,
        vector_store: Optional[VectorStoreInterface] = None,
        embedding_provider: Optional[EmbeddingProvider] = None,
    ):
        self.vector_store = vector_store or InMemoryVectorStore()
        self.embedding_provider = embedding_provider or DeterministicEmbeddingProvider()
        self._chunks_index: Dict[str, KnowledgeChunk] = {}  # chunk_id -> chunk

    def index_chunk(self, chunk: KnowledgeChunk) -> None:
        """Indexes a chunk into lexical and dense vector indices."""
        self._chunks_index[chunk.chunk_id] = chunk
        vector = self.embedding_provider.embed(chunk.content)
        emb = KnowledgeEmbedding(
            chunk_id=chunk.chunk_id,
            model_name=self.embedding_provider.model_info().get("model", "embedding"),
            dimension=len(vector),
            vector=vector,
        )
        chunk.embedding_reference = emb.embedding_id
        self.vector_store.insert(emb, chunk)

    def search_lexical(
        self,
        query: str,
        top_k: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[KnowledgeChunk, float]]:
        """Performs BM25 lexical keyword search across indexed chunks."""
        q_tokens = query.lower().split()
        scores: List[Tuple[KnowledgeChunk, float]] = []

        for chunk in self._chunks_index.values():
            if filter_dict:
                match = True
                for k, expected in filter_dict.items():
                    val = getattr(chunk, k, None) or chunk.metadata.get(k)
                    if val != expected:
                        match = False
                        break
                if not match:
                    continue

            d_tokens = chunk.content.lower().split()
            score = bm25_score(q_tokens, d_tokens)
            if score > 0.0:
                scores.append((chunk, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def search_semantic(
        self,
        query: str,
        top_k: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[KnowledgeChunk, float]]:
        """Performs dense vector similarity search."""
        query_vector = self.embedding_provider.embed(query)
        return self.vector_store.search(query_vector, top_k=top_k, filter_dict=filter_dict)

    def search_hybrid(
        self,
        query: str,
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
        rrf_k: int = 60,
    ) -> List[RetrievalResult]:
        """
        Executes hybrid retrieval and fuses results via Reciprocal Rank Fusion (RRF).
        """
        lexical_hits = self.search_lexical(query, top_k=top_k * 2, filter_dict=filter_dict)
        semantic_hits = self.search_semantic(query, top_k=top_k * 2, filter_dict=filter_dict)

        # Build RRF scores
        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, KnowledgeChunk] = {}
        lex_map: Dict[str, float] = {}
        sem_map: Dict[str, float] = {}

        # 1. Lexical ranks
        for rank, (chunk, score) in enumerate(lexical_hits, start=1):
            cid = chunk.chunk_id
            chunk_map[cid] = chunk
            lex_map[cid] = score
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (rrf_k + rank))

        # 2. Semantic ranks
        for rank, (chunk, score) in enumerate(semantic_hits, start=1):
            cid = chunk.chunk_id
            chunk_map[cid] = chunk
            sem_map[cid] = score
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (rrf_k + rank))

        # 3. Compile ranked results
        sorted_cids = sorted(rrf_scores.keys(), key=lambda cid: rrf_scores[cid], reverse=True)

        results: List[RetrievalResult] = []
        for cid in sorted_cids[:top_k]:
            chk = chunk_map[cid]
            results.append(
                RetrievalResult(
                    chunk=chk,
                    score=rrf_scores[cid],
                    semantic_score=sem_map.get(cid, 0.0),
                    keyword_score=lex_map.get(cid, 0.0),
                )
            )

        logger.info(f"Hybrid retrieval for query '{query}': returned {len(results)} results")
        return results
