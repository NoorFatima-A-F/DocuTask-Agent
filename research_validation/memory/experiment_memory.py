"""
Scientific Experiment Memory (Phase 84C)
=======================================
Stores and retrieves historical experiment outcomes, configurations,
and metric observations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class ExperimentMemoryEntry:
    """Historical record of an executed experiment."""
    entry_id: str
    experiment_id: str
    manifest_digest: str
    parameters: Dict[str, Any]
    metrics: Dict[str, float]
    status: str
    duration_ms: float
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    importance_weight: float = 1.0
    access_count: int = 0
    entry_digest_sha256: str = field(default="")


class ExperimentMemoryStore:
    """In-memory and indexed store for experiment executions."""

    def __init__(self):
        self.entries: Dict[str, ExperimentMemoryEntry] = {}
        self.index_by_experiment: Dict[str, List[str]] = {}

    def record_experiment(
        self,
        experiment_id: str,
        manifest_digest: str,
        parameters: Dict[str, Any],
        metrics: Dict[str, float],
        status: str,
        duration_ms: float,
        importance_weight: float = 1.0,
    ) -> ExperimentMemoryEntry:
        entry_id = f"mem_exp_{experiment_id}_{len(self.entries)}"
        payload = {
            "entry_id": entry_id,
            "experiment_id": experiment_id,
            "manifest_digest": manifest_digest,
            "parameters": parameters,
            "metrics": metrics,
            "status": status,
        }
        digest = hash_canonical_json(payload)

        entry = ExperimentMemoryEntry(
            entry_id=entry_id,
            experiment_id=experiment_id,
            manifest_digest=manifest_digest,
            parameters=parameters,
            metrics=metrics,
            status=status,
            duration_ms=duration_ms,
            importance_weight=importance_weight,
            entry_digest_sha256=digest,
        )

        self.entries[entry_id] = entry
        self.index_by_experiment.setdefault(experiment_id, []).append(entry_id)
        return entry

    def get_entries_for_experiment(self, experiment_id: str) -> List[ExperimentMemoryEntry]:
        entry_ids = self.index_by_experiment.get(experiment_id, [])
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]

    def find_best_performing(self, metric_name: str, higher_is_better: bool = True) -> Optional[ExperimentMemoryEntry]:
        valid = [e for e in self.entries.values() if metric_name in e.metrics and e.status == "COMPLETED"]
        if not valid:
            return None
        return max(valid, key=lambda e: e.metrics[metric_name] if higher_is_better else -e.metrics[metric_name])
