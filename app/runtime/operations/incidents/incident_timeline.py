"""
AOIS-HROP Phase 13.7 - Incident Timeline Builder
Reconstructs chronologically ordered incident evolution milestones.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class IncidentTimelineEntry:
    timestamp_utc: str
    phase: str  # DETECTED, CORRELATED, DIAGNOSED, HEALING_INITIATED, RECOVERED, VERIFIED
    description: str
    actor: str = "AOIS_AUTONOMIC_ENGINE"
    metadata: Dict[str, Any] = field(default_factory=dict)


class IncidentTimelineBuilder:
    """
    Builds and maintains audit-compliant chronological records for an incident.
    """

    def __init__(self):
        self._timelines: Dict[str, List[IncidentTimelineEntry]] = {}

    def add_entry(
        self,
        incident_id: str,
        phase: str,
        description: str,
        actor: str = "AOIS_AUTONOMIC_ENGINE",
        metadata: Dict[str, Any] = None,
    ) -> IncidentTimelineEntry:
        entry = IncidentTimelineEntry(
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            phase=phase,
            description=description,
            actor=actor,
            metadata=metadata or {},
        )
        if incident_id not in self._timelines:
            self._timelines[incident_id] = []
        self._timelines[incident_id].append(entry)
        return entry

    def get_timeline(self, incident_id: str) -> List[IncidentTimelineEntry]:
        return self._timelines.get(incident_id, [])
