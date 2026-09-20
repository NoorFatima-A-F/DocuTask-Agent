"""
Evidence Provenance & Scientific Lineage Framework
Module: evidence_store.py

Immutable, append-only scientific evidence store:
- Enforces strict ZERO-OVERWRITE policy.
- Every modification creates a new versioned entry linking previous version.
- Preserves complete immutable version histories.
- Provides multi-dimensional querying by stage, quality level, and temporal window.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from research_validation.provenance.provenance_models import (
    EvidenceNode, EvidenceQualityLevel, LineageStage
)


@dataclass
class VersionedEvidenceRecord:
    """A versioned entry in the append-only evidence store."""
    record_id: str
    version_number: int
    previous_version_record_id: Optional[str]
    evidence_node: EvidenceNode
    stored_at_epoch: float = field(default_factory=time.time)


class EvidenceStore:
    """
    Immutable append-only persistence store for scientific evidence nodes.
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir
        self.records: Dict[str, VersionedEvidenceRecord] = {}  # record_id -> record
        self.logical_versions: Dict[str, List[str]] = {}       # logical_name/node_id -> [record_id, ...]

    def store_evidence_node(self, node: EvidenceNode, logical_key: Optional[str] = None) -> VersionedEvidenceRecord:
        """
        Append an evidence node. If a logical_key already has versions, creates version N+1.
        Direct overwrite of existing record_id is strictly forbidden.
        """
        key = logical_key or node.node_id

        if node.node_id in self.records:
            raise PermissionError(
                f"IMMUTABILITY_VIOLATION: Node ID '{node.node_id}' is already stored. Direct overwrite is strictly forbidden."
            )

        history = self.logical_versions.get(key, [])
        version_num = len(history) + 1
        prev_record_id = history[-1] if history else None

        record = VersionedEvidenceRecord(
            record_id=node.node_id,
            version_number=version_num,
            previous_version_record_id=prev_record_id,
            evidence_node=node
        )

        self.records[node.node_id] = record
        self.logical_versions.setdefault(key, []).append(node.node_id)

        # Optional disk flush
        if self.storage_dir:
            self._persist_record_to_disk(record)

        return record

    def get_latest_version(self, logical_key: str) -> Optional[VersionedEvidenceRecord]:
        """Get latest version of a logical evidence key."""
        history = self.logical_versions.get(logical_key)
        if not history:
            return None
        return self.records.get(history[-1])

    def get_version_history(self, logical_key: str) -> List[VersionedEvidenceRecord]:
        """Retrieve full chronological version history."""
        history = self.logical_versions.get(logical_key, [])
        return [self.records[rid] for rid in history if rid in self.records]

    def query_by_stage(self, stage: LineageStage) -> List[VersionedEvidenceRecord]:
        """Find all records matching a specific lineage stage."""
        return [r for r in self.records.values() if r.evidence_node.stage == stage]

    def query_by_quality(self, min_quality_level: EvidenceQualityLevel) -> List[VersionedEvidenceRecord]:
        """Find records meeting or exceeding a minimum quality level."""
        min_weight = min_quality_level.numeric_weight
        return [r for r in self.records.values() if r.evidence_node.quality_level.numeric_weight >= min_weight]

    def _persist_record_to_disk(self, record: VersionedEvidenceRecord) -> None:
        """Persist record JSON immutably to disk."""
        if not self.storage_dir:
            return
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.storage_dir / f"{record.record_id}_v{record.version_number}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({
                "record_id": record.record_id,
                "version_number": record.version_number,
                "previous_version_record_id": record.previous_version_record_id,
                "stored_at_epoch": record.stored_at_epoch,
                "evidence_node": record.evidence_node.to_dict()
            }, f, indent=2)
