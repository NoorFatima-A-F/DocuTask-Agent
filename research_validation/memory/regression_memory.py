"""
Scientific Regression Memory (Phase 84C)
=======================================
Stores historical regressions, degraded metrics, and their root-cause traces.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class RegressionMemoryEntry:
    """Historical record of a detected scientific or performance regression."""
    regression_id: str
    experiment_id: str
    metric_name: str
    baseline_value: float
    regressed_value: float
    relative_degradation_pct: float
    root_cause_hypothesis: str
    resolution_status: str  # "ACTIVE", "RESOLVED", "ACCEPTED_TRADEOFF"
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    regression_digest_sha256: str = field(default="")


class RegressionMemoryStore:
    """Indexed store of performance and statistical regressions."""

    def __init__(self):
        self.regressions: Dict[str, RegressionMemoryEntry] = {}

    def record_regression(
        self,
        experiment_id: str,
        metric_name: str,
        baseline_value: float,
        regressed_value: float,
        root_cause_hypothesis: str = "",
        resolution_status: str = "ACTIVE",
    ) -> RegressionMemoryEntry:
        rel_deg = (
            ((baseline_value - regressed_value) / abs(baseline_value)) * 100.0
            if baseline_value != 0 else 0.0
        )
        regression_id = f"reg_{experiment_id}_{metric_name}_{len(self.regressions)}"
        payload = {
            "regression_id": regression_id,
            "experiment_id": experiment_id,
            "metric_name": metric_name,
            "baseline_value": baseline_value,
            "regressed_value": regressed_value,
            "relative_degradation_pct": rel_deg,
            "root_cause": root_cause_hypothesis,
        }
        digest = hash_canonical_json(payload)

        entry = RegressionMemoryEntry(
            regression_id=regression_id,
            experiment_id=experiment_id,
            metric_name=metric_name,
            baseline_value=baseline_value,
            regressed_value=regressed_value,
            relative_degradation_pct=rel_deg,
            root_cause_hypothesis=root_cause_hypothesis,
            resolution_status=resolution_status,
            regression_digest_sha256=digest,
        )
        self.regressions[regression_id] = entry
        return entry

    def get_active_regressions(self) -> List[RegressionMemoryEntry]:
        return [r for r in self.regressions.values() if r.resolution_status == "ACTIVE"]
