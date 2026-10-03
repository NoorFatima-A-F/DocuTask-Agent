"""
Dataset Lineage & Provenance Tracker.
Tracks origin, transformation, cleaning, annotation, and verification usage.
"""
from typing import Dict, List, Optional
from app.platform_verification.dataset_governance.domain.models import DatasetLineageNode
from app.platform_verification.dataset_governance.domain.interfaces import DatasetLineageTrackerInterface


class DatasetLineageTracker(DatasetLineageTrackerInterface):
    def __init__(self):
        self._lineage_records: Dict[str, List[DatasetLineageNode]] = {}

    def record_lineage(
        self,
        dataset_id: str,
        version: str,
        source: str,
        transformation: str,
        cleaners: Optional[List[str]] = None,
        annotator: str = "Verified Annotator"
    ) -> DatasetLineageNode:
        node = DatasetLineageNode(
            dataset_id=dataset_id,
            version=version,
            source_origin=source,
            transformation_step=transformation,
            applied_cleaners=cleaners or ["whitespace_trimming", "utf8_sanitization"],
            annotated_by=annotator
        )
        key = f"{dataset_id}:{version}"
        if key not in self._lineage_records:
            self._lineage_records[key] = []
        self._lineage_records[key].append(node)
        return node

    def get_lineage(self, dataset_id: str, version: str) -> List[DatasetLineageNode]:
        return self._lineage_records.get(f"{dataset_id}:{version}", [])


dataset_lineage_tracker = DatasetLineageTracker()
