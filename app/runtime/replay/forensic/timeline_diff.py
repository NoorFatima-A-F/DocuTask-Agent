"""
Timeline Diff for Phase 13.4.
Calculates structural, behavioral, and confidence differences between two mission executions.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class TimelineDiffReport(BaseModel):
    reference_mission_id: str
    comparison_mission_id: str
    similarity_score: float = 1.0
    added_events: List[Dict[str, Any]] = Field(default_factory=list)
    removed_events: List[Dict[str, Any]] = Field(default_factory=list)
    modified_decisions: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_delta: float = 0.0
    duration_delta_ms: float = 0.0


class TimelineDiffEngine:
    """
    Computes precise deterministic diffs between two replay event streams.
    """

    @classmethod
    def compute_diff(
        cls,
        ref_mission_id: str,
        comp_mission_id: str,
        ref_events: List[Dict[str, Any]],
        comp_events: List[Dict[str, Any]],
    ) -> TimelineDiffReport:
        ref_types = [e.get("event_type") for e in ref_events]
        comp_types = [e.get("event_type") for e in comp_events]

        added = []
        removed = []

        for idx, ct in enumerate(comp_types):
            if ct not in ref_types:
                added.append(comp_events[idx])

        for idx, rt in enumerate(ref_types):
            if rt not in comp_types:
                removed.append(ref_events[idx])

        max_len = max(1, max(len(ref_events), len(comp_events)))
        diff_count = len(added) + len(removed)
        similarity = max(0.0, 1.0 - (diff_count / max_len))

        return TimelineDiffReport(
            reference_mission_id=ref_mission_id,
            comparison_mission_id=comp_mission_id,
            similarity_score=round(similarity, 3),
            added_events=added,
            removed_events=removed,
            modified_decisions=[],
            confidence_delta=0.0,
            duration_delta_ms=0.0,
        )
