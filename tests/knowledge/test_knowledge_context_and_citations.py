"""
Tests for ContextBuilder and CitationEngine.
"""

from app.knowledge.citations.engine import CitationEngine
from app.knowledge.context.builder import ContextBuilder
from app.knowledge.core.models import KnowledgeChunk, RetrievalResult


def test_citation_engine_creation_and_grounding():
    engine = CitationEngine()

    chunk = KnowledgeChunk(
        chunk_id="chk-policy-42",
        document_id="doc-refunds",
        knowledge_id="kobj-policies",
        content="The refund policy guarantees full reimbursement within 30 calendar days of invoice date.",
        page_number=4,
    )

    cite = engine.create_citation(chunk, source_title="Customer Refund Policy v2", version_number="2.0.0")
    assert cite.chunk_id == "chk-policy-42"
    assert cite.page_number == 4
    assert "refund policy guarantees" in cite.snippet

    # Grounding verification
    grounded_answer = "Under the customer refund policy, full reimbursement is guaranteed within 30 days."
    grounding_score = engine.verify_grounding(grounded_answer, [cite])
    assert grounding_score > 0.4

    hallucinated_answer = "Astronauts landed on Mars in the year 2045."
    bad_score = engine.verify_grounding(hallucinated_answer, [cite])
    assert bad_score == 0.0


def test_context_builder_budgeting_and_deduplication():
    citation_engine = CitationEngine()
    builder = ContextBuilder(citation_engine=citation_engine)

    chunk1 = KnowledgeChunk(
        chunk_id="chk-1",
        document_id="doc-1",
        knowledge_id="kobj-1",
        content="Section 1: Data retention is set to 365 days.",
        token_count=10,
        metadata={"title": "Data Governance Policy"},
    )
    chunk2 = KnowledgeChunk(
        chunk_id="chk-2",
        document_id="doc-1",
        knowledge_id="kobj-1",
        content="Section 1: Data retention is set to 365 days.",  # Duplicate text
        token_count=10,
        metadata={"title": "Data Governance Policy"},
    )
    chunk3 = KnowledgeChunk(
        chunk_id="chk-3",
        document_id="doc-2",
        knowledge_id="kobj-2",
        content="Section 2: Encryption in transit uses TLS 1.3.",
        token_count=10,
        metadata={"title": "Network Security"},
    )

    candidates = [
        RetrievalResult(chunk=chunk1, score=0.9),
        RetrievalResult(chunk=chunk2, score=0.88),
        RetrievalResult(chunk=chunk3, score=0.85),
    ]

    pkg = builder.build_context(candidates, max_tokens=100)

    # Duplicate chunk2 must be deduplicated
    assert len(pkg.chunks) == 2
    assert len(pkg.citations) == 2
    assert len(pkg.sources) == 2
    assert "Data Governance Policy" in pkg.sources
    assert "Network Security" in pkg.sources
    assert pkg.confidence > 0.8
