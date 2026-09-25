"""Tier 4: Semantic Memory (Domain Knowledge & Learned Facts).

Stores declarative domain knowledge, vendor master profiles, tax regulations,
document schemas, and permanent learned rules.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.agents.memory.intelligence.retrieval_scorer import RetrievalScorer


@dataclass
class SemanticFact:
    """A persistent domain concept or learned fact."""

    fact_id: str = field(default_factory=lambda: f"fact_{uuid.uuid4().hex[:10]}")
    subject: str = ""
    predicate: str = ""
    fact_value: Any = None
    domain: str = "FINANCIAL"
    confidence: float = 1.0
    importance: float = 0.8
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_searchable_text(self) -> str:
        return f"{self.subject} {self.predicate} {str(self.fact_value)} {self.domain} {' '.join(self.tags)}"


class SemanticMemory:
    """Declarative domain knowledge store with semantic retrieval."""

    def __init__(self, scorer: Optional[RetrievalScorer] = None) -> None:
        self.scorer = scorer or RetrievalScorer()
        self._facts: Dict[str, SemanticFact] = {}
        self._seed_default_facts()

    def _seed_default_facts(self) -> None:
        """Seed baseline enterprise facts for document processing."""
        self.store_fact(
            SemanticFact(
                subject="ACME Corporation",
                predicate="tax_id",
                fact_value="US-123456789",
                domain="FINANCIAL",
                importance=0.9,
                tags=["vendor", "tax", "acme", "invoice"],
            )
        )
        self.store_fact(
            SemanticFact(
                subject="Standard Invoice Rule",
                predicate="total_formula",
                fact_value="total_amount = subtotal + tax_amount",
                domain="ACCOUNTING",
                importance=1.0,
                tags=["formula", "validation", "arithmetic", "invoice"],
            )
        )
        self.store_fact(
            SemanticFact(
                subject="SOX Compliance Standard",
                predicate="retention_period_years",
                fact_value=7,
                domain="COMPLIANCE",
                importance=0.95,
                tags=["sox", "compliance", "retention", "audit"],
            )
        )
        self.store_fact(
            SemanticFact(
                subject="Tesseract OCR Degradation",
                predicate="correction_heuristic",
                fact_value="If confidence < 0.90 or handwriting detected, route to Gemini Multimodal Vision",
                domain="OCR",
                importance=0.9,
                tags=["ocr", "tesseract", "gemini", "correction", "fallback"],
            )
        )

    def store_fact(self, fact: SemanticFact) -> str:
        self._facts[fact.fact_id] = fact
        return fact.fact_id

    def get_fact(self, fact_id: str) -> Optional[SemanticFact]:
        return self._facts.get(fact_id)

    def retrieve_relevant_facts(
        self,
        query: str,
        task_tags: Optional[List[str]] = None,
        top_k: int = 5,
        min_score: float = 0.20,
    ) -> List[tuple[SemanticFact, float]]:
        """Retrieve most relevant facts based on multi-factor scoring formula."""
        tags = task_tags or []
        now = time.time()
        scored: List[tuple[SemanticFact, float]] = []

        for fact in self._facts.values():
            text = fact.to_searchable_text()
            score = self.scorer.calculate_score(
                query=query,
                memory_content=text,
                importance=fact.importance,
                timestamp=fact.created_at,
                memory_tags=fact.tags,
                current_task_tags=tags,
                current_time=now,
            )
            if score >= min_score:
                scored.append((fact, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def count(self) -> int:
        return len(self._facts)
