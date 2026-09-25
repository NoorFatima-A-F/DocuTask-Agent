"""
Confidence Lineage Engine for Phase 13.3 (ASCE-CGP).
Generates cryptographic hash chains linking raw evidence to final confidence values.
"""

import hashlib
import json
from typing import Dict, List, Any
from datetime import datetime, timezone
from app.runtime.confidence.models.confidence_models import ConfidenceLineageRecord


class ConfidenceLineageEngine:
    """
    Maintains reproducible cryptographic provenance for every confidence calculation.
    """

    _lineage_records: List[ConfidenceLineageRecord] = []

    @classmethod
    def record_lineage(
        cls,
        mission_id: str,
        dimension: str,
        score: float,
        uncertainty: float,
        evidence_signals: Dict[str, Any],
        features: Dict[str, float],
        formula_version: str,
        truth_ledger_hash: str,
        replay_offset: int,
    ) -> ConfidenceLineageRecord:
        ev_hash = hashlib.sha256(json.dumps(evidence_signals, sort_keys=True).encode('utf-8')).hexdigest()
        feat_hash = hashlib.sha256(json.dumps(features, sort_keys=True).encode('utf-8')).hexdigest()

        record = ConfidenceLineageRecord(
            lineage_id=f"lin-{mission_id}-{dimension.lower()}",
            mission_id=mission_id,
            dimension=dimension,
            score=score,
            uncertainty=uncertainty,
            evidence_snapshot_hash=ev_hash,
            feature_vector_hash=feat_hash,
            formula_version=formula_version,
            truth_ledger_hash=truth_ledger_hash,
            replay_offset=replay_offset,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        cls._lineage_records.append(record)
        return record

    @classmethod
    def get_lineage_for_mission(cls, mission_id: str) -> List[ConfidenceLineageRecord]:
        return [r for r in cls._lineage_records if r.mission_id == mission_id]
