"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Context Intelligence Engine.
Builds token-budgeted, deduplicated, and citation-grounded context packages for AI agents and workflows.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.knowledge.citations.engine import CitationEngine
from app.knowledge.core.models import Citation, KnowledgeChunk, RetrievalResult

logger = logging.getLogger(__name__)


class ContextPackage(BaseModel):
    """Structured context artifact delivered to AI agents."""
    context_text: str
    chunks: List[KnowledgeChunk] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    confidence: float = 1.0
    token_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ContextBuilder:
    """
    Compresses and formats retrieved knowledge chunks into unified agent prompt context.
    """

    def __init__(self, citation_engine: Optional[CitationEngine] = None):
        self.citation_engine = citation_engine or CitationEngine()

    def build_context(
        self,
        retrieval_results: List[RetrievalResult],
        max_tokens: int = 2000,
        include_citations: bool = True,
    ) -> ContextPackage:
        """
        Selects top evidence, deduplicates overlapping texts, formats context string,
        and generates formal citations.
        """
        selected_chunks: List[KnowledgeChunk] = []
        citations: List[Citation] = []
        sources: set[str] = set()
        seen_texts: set[str] = set()

        total_tokens = 0
        context_blocks: List[str] = []

        for res in retrieval_results:
            chunk = res.chunk
            content = chunk.content.strip()

            # Deduplication
            if content in seen_texts:
                continue
            seen_texts.add(content)

            chunk_tokens = chunk.token_count or int(len(content.split()) * 1.3)
            if total_tokens + chunk_tokens > max_tokens and selected_chunks:
                break

            selected_chunks.append(chunk)
            total_tokens += chunk_tokens

            doc_title = chunk.metadata.get("title", f"Doc-{chunk.document_id}")
            sources.add(doc_title)

            # Generate citation
            if include_citations:
                cite = self.citation_engine.create_citation(
                    chunk=chunk,
                    source_title=doc_title,
                    version_number=chunk.metadata.get("version", "1.0.0"),
                    confidence=min(1.0, max(0.0, res.score)),
                )
                citations.append(cite)
                context_blocks.append(f"[{cite.citation_id}] ({doc_title}, Page {chunk.page_number}):\n{content}")
            else:
                context_blocks.append(content)

        formatted_context = "\n\n---\n\n".join(context_blocks)
        avg_confidence = (
            sum(r.score for r in retrieval_results[: len(selected_chunks)]) / max(1, len(selected_chunks))
            if selected_chunks
            else 0.0
        )

        return ContextPackage(
            context_text=formatted_context,
            chunks=selected_chunks,
            sources=sorted(list(sources)),
            citations=citations,
            confidence=min(1.0, max(0.0, avg_confidence)),
            token_count=total_tokens,
            metadata={"selected_chunks_count": len(selected_chunks)},
        )
