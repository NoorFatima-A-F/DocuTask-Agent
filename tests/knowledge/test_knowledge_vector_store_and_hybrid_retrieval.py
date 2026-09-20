"""
Tests for VectorStoreInterface and HybridRetrievalEngine.
"""

import pytest
from app.knowledge.core.models import KnowledgeChunk, KnowledgeEmbedding
from app.knowledge.embeddings.provider import DeterministicEmbeddingProvider
from app.knowledge.retrieval.engine import HybridRetrievalEngine, bm25_score
from app.knowledge.vector.store import InMemoryVectorStore, cosine_similarity


def test_vector_store_operations_and_similarity():
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    v3 = [0.0, 1.0, 0.0]

    assert cosine_similarity(v1, v2) == 1.0
    assert cosine_similarity(v1, v3) == 0.0

    store = InMemoryVectorStore()

    chunk1 = KnowledgeChunk(
        chunk_id="chk-finance-1",
        document_id="doc-1",
        knowledge_id="kobj-finance",
        content="Invoice accounts payable processing guidelines",
        metadata={"department": "finance"},
    )
    emb1 = KnowledgeEmbedding(
        embedding_id="emb-1",
        chunk_id="chk-finance-1",
        dimension=3,
        vector=[0.9, 0.1, 0.0],
    )

    chunk2 = KnowledgeChunk(
        chunk_id="chk-hr-1",
        document_id="doc-2",
        knowledge_id="kobj-hr",
        content="Vacation and leave policy for remote employees",
        metadata={"department": "hr"},
    )
    emb2 = KnowledgeEmbedding(
        embedding_id="emb-2",
        chunk_id="chk-hr-1",
        dimension=3,
        vector=[0.0, 0.8, 0.6],
    )

    store.insert(emb1, chunk1)
    store.insert(emb2, chunk2)
    assert store.count() == 2

    # Query matching finance
    results = store.search(query_vector=[1.0, 0.0, 0.0], top_k=2)
    assert len(results) == 2
    assert results[0][0].chunk_id == "chk-finance-1"
    assert results[0][1] > results[1][1]

    # Filtered search
    filtered = store.search(query_vector=[1.0, 0.0, 0.0], top_k=2, filter_dict={"department": "hr"})
    assert len(filtered) == 1
    assert filtered[0][0].chunk_id == "chk-hr-1"

    # Deletion
    assert store.delete("chk-finance-1") is True
    assert store.count() == 1


def test_hybrid_retrieval_engine_rrf_fusion():
    provider = DeterministicEmbeddingProvider(dimension=64)
    store = InMemoryVectorStore()
    retrieval = HybridRetrievalEngine(vector_store=store, embedding_provider=provider)

    chunks = [
        KnowledgeChunk(
            chunk_id="chk-1",
            document_id="doc-1",
            knowledge_id="kobj-1",
            content="Enterprise Single Sign-On (SSO) SAML and OIDC authentication guide",
        ),
        KnowledgeChunk(
            chunk_id="chk-2",
            document_id="doc-2",
            knowledge_id="kobj-2",
            content="Database indexing and query performance tuning strategies",
        ),
        KnowledgeChunk(
            chunk_id="chk-3",
            document_id="doc-3",
            knowledge_id="kobj-3",
            content="Customer refund policies and 30-day return procedures",
        ),
    ]

    for chk in chunks:
        retrieval.index_chunk(chk)

    # Hybrid query for authentication
    results = retrieval.search_hybrid("SAML authentication SSO", top_k=2)
    assert len(results) >= 1
    assert results[0].chunk.chunk_id == "chk-1"
    assert results[0].score > 0.0
    assert results[0].keyword_score > 0.0
