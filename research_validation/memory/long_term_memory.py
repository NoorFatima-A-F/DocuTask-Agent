"""
Scientific Long-Term Memory (Phase 84C)
======================================
Stores persistent consolidated knowledge with temporal decay and access reinforcement.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class LongTermMemoryItem:
    """A consolidated fact, invariant, or empirical law."""
    item_id: str
    concept: str
    assertion: str
    evidence_weight: float
    access_count: int
    created_timestamp: float
    last_accessed_timestamp: float
    half_life_days: float = 30.0
    item_digest_sha256: str = field(default="")

    def current_retention_strength(self, current_timestamp: float) -> float:
        """Calculates exponential retention decay: R = e^(-lambda * dt)."""
        dt_days = max(0.0, (current_timestamp - self.last_accessed_timestamp) / 86400.0)
        decay_lambda = math.log(2.0) / max(1.0, self.half_life_days)
        base_decay = math.exp(-decay_lambda * dt_days)
        # Access count provides reinforcement against decay
        reinforcement = 1.0 + math.log1p(self.access_count) * 0.2
        return min(1.0, self.evidence_weight * base_decay * reinforcement)


class LongTermMemoryStore:
    """Long-term memory repository with decay and consolidation mechanisms."""

    def __init__(self, forgetting_threshold: float = 0.05):
        self.forgetting_threshold = forgetting_threshold
        self.items: Dict[str, LongTermMemoryItem] = {}

    def store_invariant(
        self,
        concept: str,
        assertion: str,
        evidence_weight: float = 1.0,
        half_life_days: float = 30.0,
        current_time: Optional[float] = None,
    ) -> LongTermMemoryItem:
        t = current_time or datetime.now(timezone.utc).timestamp()
        item_id = f"ltm_{concept}_{len(self.items)}"
        payload = {
            "item_id": item_id,
            "concept": concept,
            "assertion": assertion,
            "evidence_weight": evidence_weight,
        }
        digest = hash_canonical_json(payload)

        item = LongTermMemoryItem(
            item_id=item_id,
            concept=concept,
            assertion=assertion,
            evidence_weight=evidence_weight,
            access_count=1,
            created_timestamp=t,
            last_accessed_timestamp=t,
            half_life_days=half_life_days,
            item_digest_sha256=digest,
        )
        self.items[item_id] = item
        return item

    def recall(self, concept: str, current_time: Optional[float] = None) -> List[LongTermMemoryItem]:
        """Recalls non-forgotten assertions for a concept, updating access counters."""
        t = current_time or datetime.now(timezone.utc).timestamp()
        recalled: List[LongTermMemoryItem] = []
        for item_id, item in list(self.items.items()):
            if item.concept == concept:
                strength = item.current_retention_strength(t)
                if strength >= self.forgetting_threshold:
                    # Update item with incremented access
                    updated = LongTermMemoryItem(
                        item_id=item.item_id,
                        concept=item.concept,
                        assertion=item.assertion,
                        evidence_weight=item.evidence_weight,
                        access_count=item.access_count + 1,
                        created_timestamp=item.created_timestamp,
                        last_accessed_timestamp=t,
                        half_life_days=item.half_life_days,
                        item_digest_sha256=item.item_digest_sha256,
                    )
                    self.items[item_id] = updated
                    recalled.append(updated)
        return recalled

    def prune_decayed_memories(self, current_time: Optional[float] = None) -> int:
        """Removes items whose retention strength has decayed below threshold."""
        t = current_time or datetime.now(timezone.utc).timestamp()
        to_delete = [
            iid for iid, item in self.items.items()
            if item.current_retention_strength(t) < self.forgetting_threshold
        ]
        for iid in to_delete:
            del self.items[iid]
        return len(to_delete)
