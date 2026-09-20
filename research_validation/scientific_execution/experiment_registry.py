"""
Experiment Registry (Phase 82B.1)
=================================
Strongly-typed, append-only registry for scientific experiments.
Enforces registration before execution, guarantees uniqueness, and preserves
complete audit history.
"""

from __future__ import annotations
import json
import os
import threading
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

from research_validation.scientific_execution.experiment_manifest import (
    ExperimentManifest, ExperimentStatus
)
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class ExperimentRecord:
    manifest: ExperimentManifest
    status: ExperimentStatus
    registered_at_utc: str
    execution_count: int = 0
    latest_run_hash: Optional[str] = None
    historical_run_hashes: Tuple[str, ...] = ()


class ExperimentRegistry:
    """
    Immutable catalog of registered scientific experiments.
    Nothing executes without prior registration.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = storage_dir
        self._lock = threading.Lock()
        self._records: Dict[str, ExperimentRecord] = {}

    def register(self, manifest: ExperimentManifest) -> ExperimentRecord:
        """Register a new experiment manifest."""
        with self._lock:
            if manifest.experiment_id in self._records:
                raise ValueError(
                    f"Experiment '{manifest.experiment_id}' is already registered. "
                    "Overwriting experiment manifests is strictly forbidden."
                )

            record = ExperimentRecord(
                manifest=manifest,
                status=ExperimentStatus.REGISTERED,
                registered_at_utc=datetime.now(timezone.utc).isoformat(),
            )
            self._records[manifest.experiment_id] = record

            if self.storage_dir:
                self._persist_record(record)

            return record

    def get_record(self, experiment_id: str) -> Optional[ExperimentRecord]:
        """Retrieve registered record by ID."""
        with self._lock:
            return self._records.get(experiment_id)

    def update_status(
        self,
        experiment_id: str,
        new_status: ExperimentStatus,
        run_hash: Optional[str] = None,
    ) -> ExperimentRecord:
        """Update experiment status and record execution run hash."""
        with self._lock:
            if experiment_id not in self._records:
                raise KeyError(f"Experiment '{experiment_id}' not found in registry.")

            current = self._records[experiment_id]
            runs = list(current.historical_run_hashes)
            if run_hash:
                runs.append(run_hash)

            updated = ExperimentRecord(
                manifest=current.manifest,
                status=new_status,
                registered_at_utc=current.registered_at_utc,
                execution_count=current.execution_count + (1 if run_hash else 0),
                latest_run_hash=run_hash or current.latest_run_hash,
                historical_run_hashes=tuple(runs),
            )
            self._records[experiment_id] = updated

            if self.storage_dir:
                self._persist_record(updated)

            return updated

    def list_experiments(
        self,
        tag: Optional[str] = None,
        status: Optional[ExperimentStatus] = None,
    ) -> List[ExperimentRecord]:
        """Query registered experiments."""
        with self._lock:
            results = list(self._records.values())
            if tag:
                results = [r for r in results if tag in r.manifest.tags]
            if status:
                results = [r for r in results if r.status == status]
            return results

    def _persist_record(self, record: ExperimentRecord) -> None:
        if not self.storage_dir:
            return
        os.makedirs(self.storage_dir, exist_ok=True)
        file_path = os.path.join(self.storage_dir, f"{record.manifest.experiment_id}.json")
        data = {
            "manifest": record.manifest.to_canonical_dict(),
            "status": record.status.value,
            "registered_at_utc": record.registered_at_utc,
            "execution_count": record.execution_count,
            "latest_run_hash": record.latest_run_hash,
            "historical_run_hashes": list(record.historical_run_hashes),
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
