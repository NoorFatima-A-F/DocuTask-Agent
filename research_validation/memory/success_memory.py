"""
Scientific Success Memory (Phase 84C)
====================================
Tracks high-confidence, Pareto-optimal configurations and verified claims.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List

from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class SuccessMemoryEntry:
    """Historical record of an exemplary, high-performing scientific run."""
    success_id: str
    experiment_id: str
    optimal_parameters: Dict[str, Any]
    verified_metrics: Dict[str, float]
    confidence_score: float
    reproducibility_verified: bool
    citation_or_claim_ref: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    success_digest_sha256: str = field(default="")


class SuccessMemoryStore:
    """Indexed store of verified optimal configurations."""

    def __init__(self):
        self.successes: Dict[str, SuccessMemoryEntry] = {}

    def record_success(
        self,
        experiment_id: str,
        optimal_parameters: Dict[str, Any],
        verified_metrics: Dict[str, float],
        confidence_score: float = 0.95,
        reproducibility_verified: bool = True,
        citation_or_claim_ref: str = "",
    ) -> SuccessMemoryEntry:
        success_id = f"success_{experiment_id}_{len(self.successes)}"
        payload = {
            "success_id": success_id,
            "experiment_id": experiment_id,
            "optimal_parameters": optimal_parameters,
            "verified_metrics": verified_metrics,
            "confidence_score": confidence_score,
        }
        digest = hash_canonical_json(payload)

        entry = SuccessMemoryEntry(
            success_id=success_id,
            experiment_id=experiment_id,
            optimal_parameters=optimal_parameters,
            verified_metrics=verified_metrics,
            confidence_score=confidence_score,
            reproducibility_verified=reproducibility_verified,
            citation_or_claim_ref=citation_or_claim_ref,
            success_digest_sha256=digest,
        )
        self.successes[success_id] = entry
        return entry

    def get_pareto_front(self, objective_a: str, objective_b: str) -> List[SuccessMemoryEntry]:
        """Calculates 2D Pareto-optimal configurations from stored successes."""
        candidates = [
            e for e in self.successes.values()
            if objective_a in e.verified_metrics and objective_b in e.verified_metrics
        ]
        pareto: List[SuccessMemoryEntry] = []
        for c1 in candidates:
            is_dominated = False
            for c2 in candidates:
                if c1 == c2:
                    continue
                if (
                    c2.verified_metrics[objective_a] >= c1.verified_metrics[objective_a]
                    and c2.verified_metrics[objective_b] >= c1.verified_metrics[objective_b]
                    and (
                        c2.verified_metrics[objective_a] > c1.verified_metrics[objective_a]
                        or c2.verified_metrics[objective_b] > c1.verified_metrics[objective_b]
                    )
                ):
                    is_dominated = True
                    break
            if not is_dominated:
                pareto.append(c1)
        return pareto
