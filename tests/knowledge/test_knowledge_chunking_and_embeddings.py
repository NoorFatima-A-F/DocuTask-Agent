"""
Tests for ChunkingEngine and EmbeddingProvider.
"""

import pytest
from app.knowledge.chunking.chunker import (
    ChunkingEngine,
    CodeChunker,
    FixedChunker,
    HeadingChunker,
    HierarchicalChunker,
    SemanticChunker,
)
from app.knowledge.core.models import KnowledgeDocument
from app.knowledge.embeddings.provider import DeterministicEmbeddingProvider


def test_chunking_strategies():
    engine = ChunkingEngine()

    text = """# Introduction
This is the first section of the document. It contains important overview details.

# Architecture
The architecture is divided into three layers: kernel, workflows, and multi-agent systems.

# Conclusion
In conclusion, the system provides high durability and governance.
"""

    doc = KnowledgeDocument(
        id="kdoc-chunk-test",
        knowledge_id="kobj-test",
        title="Architecture Guide",
        file_type="md",
        normalized_text=text,
    )

    # 1. Heading Chunker
    heading_chunks = engine.chunk_document(doc, strategy="heading")
    assert len(heading_chunks) == 3
    assert heading_chunks[0].heading_hierarchy == ["Introduction"]
    assert heading_chunks[1].heading_hierarchy == ["Architecture"]

    # 2. Fixed Chunker
    fixed_chunks = engine.chunk_document(doc, strategy="fixed")
    assert len(fixed_chunks) >= 1

    # 3. Semantic Chunker
    semantic_chunks = engine.chunk_document(doc, strategy="semantic")
    assert len(semantic_chunks) >= 1

    # 4. Hierarchical Chunker
    hier_chunks = engine.chunk_document(doc, strategy="hierarchical")
    parents = [c for c in hier_chunks if c.metadata.get("hierarchy_level") == "PARENT"]
    children = [c for c in hier_chunks if c.metadata.get("hierarchy_level") == "CHILD"]
    assert len(parents) > 0
    assert len(children) > 0
    assert children[0].parent_chunk_id == parents[0].chunk_id


def test_code_chunker():
    code_text = """def authenticate_user(username, password):
    if not username:
        return False
    return True

class WorkflowExecutor:
    def execute(self, plan):
        return {"status": "SUCCESS"}
"""
    doc = KnowledgeDocument(
        id="kdoc-code",
        knowledge_id="kobj-code",
        title="auth.py",
        file_type="py",
        normalized_text=code_text,
    )

    code_chunker = CodeChunker()
    chunks = code_chunker.chunk(doc)
    assert len(chunks) == 2
    assert "def authenticate_user" in chunks[0].content
    assert "class WorkflowExecutor" in chunks[1].content


def test_deterministic_embedding_provider():
    provider = DeterministicEmbeddingProvider(dimension=64)
    assert provider.dimensions() == 64

    vec1 = provider.embed("invoice payment process")
    vec2 = provider.embed("invoice payment process")
    vec3 = provider.embed("completely unrelated biology genome data")

    # Determinism
    assert vec1 == vec2
    assert len(vec1) == 64

    # Unit normalization check: sum of squares ≈ 1.0
    norm_sq = sum(x * x for x in vec1)
    assert pytest.approx(norm_sq, abs=1e-4) == 1.0

    # Batch embedding
    batch = provider.embed_batch(["alpha", "beta"])
    assert len(batch) == 2
    assert len(batch[0]) == 64
