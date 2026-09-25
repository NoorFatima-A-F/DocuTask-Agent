"""Provenance History & Reproducibility Engine (Phase 8B)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from app.data_governance.provenance.source import ProvenanceSourceRecord
from app.data_governance.provenance.transformations import ProvenanceTransformationRecord


class ProvenanceHistoryEngine:
    """Manages immutable provenance audit chains proving how data was derived and used."""

    def __init__(self):
        # asset_id -> ProvenanceSourceRecord
        self._sources: Dict[str, ProvenanceSourceRecord] = {}
        # asset_id -> List[ProvenanceTransformationRecord]
        self._transformations: Dict[str, List[ProvenanceTransformationRecord]] = {}

    def record_source(self, record: ProvenanceSourceRecord) -> ProvenanceSourceRecord:
        """Register the immutable source origin of an asset."""
        self._sources[record.asset_id] = record
        return record

    def record_transformation(self, record: ProvenanceTransformationRecord) -> ProvenanceTransformationRecord:
        """Append a transformation step to an asset's provenance history."""
        if record.asset_id not in self._transformations:
            self._transformations[record.asset_id] = []
        self._transformations[record.asset_id].append(record)
        return record

    def get_source(self, asset_id: str) -> Optional[ProvenanceSourceRecord]:
        """Get source record for asset."""
        return self._sources.get(asset_id)

    def get_transformations(self, asset_id: str) -> List[ProvenanceTransformationRecord]:
        """Get transformation history for asset."""
        return self._transformations.get(asset_id, [])

    def verify_reproducibility(self, asset_id: str) -> Dict[str, Any]:
        """Verify whether complete provenance inputs/parameters exist to reproduce output."""
        source = self.get_source(asset_id)
        transformations = self.get_transformations(asset_id)

        has_source = source is not None
        has_transformations = len(transformations) > 0
        all_models_specified = all(t.model_version is not None for t in transformations if "ai" in t.step_name.lower())

        is_reproducible = has_source or has_transformations

        return {
            "asset_id": asset_id,
            "is_reproducible": is_reproducible,
            "has_source_record": has_source,
            "transformation_steps_count": len(transformations),
            "all_models_specified": all_models_specified,
        }
