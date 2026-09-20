"""Planning Memory Engine for DocuTask Autonomous Planning Platform.

Stores past mission plan executions, outcome metrics, and contextual signatures to accelerate strategy
selection and boost utility bonuses for historically proven workflows.
"""

from __future__ import annotations

import math
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PlanSignature(BaseModel):
    """Contextual fingerprint of a mission document and goal characteristics."""
    document_type: str = "invoice"
    page_count: int = 1
    field_count: int = 10
    noise_level: float = 0.1  # [0, 1]
    domain_tags: List[str] = Field(default_factory=lambda: ["finance", "tax"])


class StrategyOutcomeRecord(BaseModel):
    """Historical execution record of an applied planning strategy."""
    record_id: str = Field(default_factory=lambda: f"mem_{uuid.uuid4().hex[:8]}")
    mission_id: str
    signature: PlanSignature
    selected_archetype: str
    selected_strategy_id: str
    actual_latency_ms: float
    actual_cost_usd: float
    actual_accuracy: float
    success: bool
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PlanningMemoryEngine:
    """Indexes and retrieves empirical mission strategy outcomes."""

    def __init__(self) -> None:
        self._records: List[StrategyOutcomeRecord] = []
        self._seed_sample_memory()

    def _seed_sample_memory(self) -> None:
        """Seeds initial empirical ground truth memory."""
        self.store_outcome(
            mission_id="mission_seed_001",
            signature=PlanSignature(document_type="invoice", page_count=2, field_count=12, noise_level=0.05, domain_tags=["finance", "invoicing"]),
            selected_archetype="DELTA_PARETO",
            selected_strategy_id="strat_delta_pareto",
            actual_latency_ms=1850.0,
            actual_cost_usd=0.0042,
            actual_accuracy=0.985,
            success=True,
        )
        self.store_outcome(
            mission_id="mission_seed_002",
            signature=PlanSignature(document_type="receipt", page_count=1, field_count=6, noise_level=0.35, domain_tags=["retail", "receipt"]),
            selected_archetype="BETA_ACCURATE",
            selected_strategy_id="strat_beta_accurate",
            actual_latency_ms=2900.0,
            actual_cost_usd=0.0125,
            actual_accuracy=0.992,
            success=True,
        )
        self.store_outcome(
            mission_id="mission_seed_003",
            signature=PlanSignature(document_type="tax_form_1040", page_count=4, field_count=45, noise_level=0.1, domain_tags=["tax", "irs", "compliance"]),
            selected_archetype="BETA_ACCURATE",
            selected_strategy_id="strat_beta_accurate",
            actual_latency_ms=3800.0,
            actual_cost_usd=0.0180,
            actual_accuracy=0.998,
            success=True,
        )

    def store_outcome(
        self,
        mission_id: str,
        signature: PlanSignature,
        selected_archetype: str,
        selected_strategy_id: str,
        actual_latency_ms: float,
        actual_cost_usd: float,
        actual_accuracy: float,
        success: bool,
    ) -> StrategyOutcomeRecord:
        record = StrategyOutcomeRecord(
            mission_id=mission_id,
            signature=signature,
            selected_archetype=selected_archetype,
            selected_strategy_id=selected_strategy_id,
            actual_latency_ms=actual_latency_ms,
            actual_cost_usd=actual_cost_usd,
            actual_accuracy=actual_accuracy,
            success=success,
        )
        self._records.append(record)
        return record

    def retrieve_similar_plans(
        self,
        signature: PlanSignature,
        top_k: int = 3,
    ) -> List[tuple[StrategyOutcomeRecord, float]]:
        """Calculates cosine/feature similarity against indexed records."""
        scored: List[tuple[StrategyOutcomeRecord, float]] = []

        for rec in self._records:
            sim = self._compute_similarity(signature, rec.signature)
            scored.append((rec, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def _compute_similarity(self, sig1: PlanSignature, sig2: PlanSignature) -> float:
        # Document type match
        type_score = 1.0 if sig1.document_type == sig2.document_type else 0.3

        # Page count similarity
        page_diff = abs(sig1.page_count - sig2.page_count)
        page_score = max(0.0, 1.0 - (page_diff / 10.0))

        # Tag overlap (Jaccard similarity)
        set1 = set(sig1.domain_tags)
        set2 = set(sig2.domain_tags)
        tag_score = len(set1 & set2) / max(1, len(set1 | set2))

        # Composite similarity
        sim = (type_score * 0.4) + (page_score * 0.3) + (tag_score * 0.3)
        return round(sim, 4)

    def get_recommended_archetype(self, signature: PlanSignature) -> Optional[str]:
        similar = self.retrieve_similar_plans(signature, top_k=3)
        if not similar or similar[0][1] < 0.6:
            return None
        return similar[0][0].selected_archetype
