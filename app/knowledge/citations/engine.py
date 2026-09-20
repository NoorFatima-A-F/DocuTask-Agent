"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Citation Engine.
Generates structured attribution citations and validates factual grounding of AI responses.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

from app.knowledge.core.models import Citation, KnowledgeChunk

logger = logging.getLogger(__name__)


class CitationEngine:
    """
    Generates deterministic evidence citations linking model assertions to specific
    document versions, page numbers, and chunk snippets.
    """

    def create_citation(
        self,
        chunk: KnowledgeChunk,
        source_title: str = "Knowledge Document",
        version_number: str = "1.0.0",
        confidence: float = 1.0,
    ) -> Citation:
        """Constructs an immutable citation record from an evidence chunk."""
        # Create snippet (first 150 chars)
        snippet = chunk.content[:150] + ("..." if len(chunk.content) > 150 else "")
        return Citation(
            citation_id=f"cite-{uuid.uuid4().hex[:8]}",
            source_title=source_title,
            document_id=chunk.document_id,
            version_number=version_number,
            page_number=chunk.page_number,
            chunk_id=chunk.chunk_id,
            snippet=snippet,
            confidence=confidence,
            timestamp=datetime.now(timezone.utc),
        )

    def verify_grounding(self, generated_text: str, citations: List[Citation]) -> float:
        """
        Computes grounding score (0.0 to 1.0) indicating content word overlap between
        generated response and cited snippets.
        """
        if not citations or not generated_text:
            return 0.0

        stopwords = {
            "the", "a", "an", "in", "on", "of", "and", "or", "is", "are", "was",
            "were", "at", "by", "for", "with", "about", "to", "from", "it", "this", "that"
        }
        gen_words = {w.strip(".,!?;:\"'") for w in generated_text.lower().split()} - stopwords
        if not gen_words:
            return 0.0

        cited_words: set[str] = set()
        for c in citations:
            words = {w.strip(".,!?;:\"'") for w in c.snippet.lower().split()} - stopwords
            cited_words.update(words)

        if not cited_words:
            return 0.0

        overlap = gen_words.intersection(cited_words)
        grounding_score = len(overlap) / min(len(gen_words), len(cited_words))
        return min(1.0, max(0.0, grounding_score))
