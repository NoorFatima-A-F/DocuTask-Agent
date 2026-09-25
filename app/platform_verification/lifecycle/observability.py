from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any

@dataclass(frozen=True)
class LifecycleTimelineEntry:
    phase_name: str
    timestamp: str
    duration_ms: float
    details: Dict[str, Any] = field(default_factory=dict)

class LifecycleTimelineTracker:
    def __init__(self):
        self._entries: List[LifecycleTimelineEntry] = []

    def record_phase(self, phase_name: str, duration_ms: float, details: Dict[str, Any]) -> None:
        entry = LifecycleTimelineEntry(
            phase_name=phase_name,
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration_ms=duration_ms,
            details=details
        )
        self._entries.append(entry)

    def get_timeline(self) -> List[LifecycleTimelineEntry]:
        return list(self._entries)
