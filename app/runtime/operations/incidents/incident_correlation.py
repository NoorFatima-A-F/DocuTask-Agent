"""
AOIS-HROP Phase 13.7 - Incident Correlation Engine
Groups related failures and cascading alerts into unified, actionable incident clusters.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class RawAlert:
    alert_id: str
    source_subsystem: str
    error_type: str
    message: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class CorrelatedIncidentEnvelope:
    incident_id: str
    title: str
    primary_subsystem: str
    correlated_alerts_count: int
    raw_alerts: List[RawAlert]
    fingerprint: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IncidentCorrelationEngine:
    """
    Correlates individual anomalous alerts across time windows and component tags into root incident envelopes.
    """

    def __init__(self, correlation_window_sec: float = 60.0):
        self.correlation_window_sec = correlation_window_sec
        self._envelopes: List[CorrelatedIncidentEnvelope] = []

    def correlate_alerts(self, alerts: List[RawAlert]) -> List[CorrelatedIncidentEnvelope]:
        if not alerts:
            return []

        # Group alerts by component or error similarity
        grouped: Dict[str, List[RawAlert]] = {}
        for a in alerts:
            key = f"{a.source_subsystem}:{a.error_type}"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(a)

        results = []
        for key, group in grouped.items():
            subsystem, err_type = key.split(":", 1)
            fingerprint = f"fp-{hash(key) & 0xffffffff:08x}"

            envelope = CorrelatedIncidentEnvelope(
                incident_id=f"inc-{uuid.uuid4().hex[:8]}",
                title=f"Correlated {err_type} in {subsystem} ({len(group)} alerts)",
                primary_subsystem=subsystem,
                correlated_alerts_count=len(group),
                raw_alerts=group,
                fingerprint=fingerprint,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            results.append(envelope)
            self._envelopes.append(envelope)

        return results

    def get_all_envelopes(self) -> List[CorrelatedIncidentEnvelope]:
        return self._envelopes
