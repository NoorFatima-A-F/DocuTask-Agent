"""
Metric Provenance Record and Merkle Lineage Verification for DocuTask Agent.
Every metric calculation produces an auditable MetricProvenanceRecord linking
the computed value back to raw RuntimeEvents via cryptographic digests and formula proofs.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def compute_merkle_root(event_ids: List[str]) -> str:
    """
    Computes deterministic SHA-256 Merkle root from a sorted list of event IDs.
    """
    if not event_ids:
        return hashlib.sha256(b"EMPTY_EVENT_STREAM").hexdigest()

    hashes = [hashlib.sha256(e_id.encode("utf-8")).digest() for e_id in sorted(event_ids)]
    while len(hashes) > 1:
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])
        next_level = []
        for i in range(0, len(hashes), 2):
            combined = hashlib.sha256(hashes[i] + hashes[i + 1]).digest()
            next_level.append(combined)
        hashes = next_level
    return hashes[0].hex()


@dataclass(frozen=True)
class MetricProvenanceRecord:
    """
    Authoritative scientific audit record for any metric computation.
    """
    metric_id: str
    metric_name: str
    metric_version: str
    value: Any
    formatted_value: str
    unit: str
    formula_id: str
    formula_expression: str
    formula_latex: str
    variables_used: Dict[str, Any]
    raw_event_ids: List[str]
    sample_size: int
    observation_window: Dict[str, Any]
    statistical_summary: Optional[Dict[str, Any]]
    merkle_events_root_sha256: str
    calculated_at_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    sentinel_state: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_id": self.metric_id,
            "metric_name": self.metric_name,
            "metric_version": self.metric_version,
            "value": self.value,
            "formatted_value": self.formatted_value,
            "unit": self.unit,
            "formula_id": self.formula_id,
            "formula_expression": self.formula_expression,
            "formula_latex": self.formula_latex,
            "variables_used": self.variables_used,
            "raw_event_ids": self.raw_event_ids,
            "sample_size": self.sample_size,
            "observation_window": self.observation_window,
            "statistical_summary": self.statistical_summary,
            "merkle_events_root_sha256": self.merkle_events_root_sha256,
            "calculated_at_utc": self.calculated_at_utc,
            "sentinel_state": self.sentinel_state,
            "tags": self.tags,
        }
