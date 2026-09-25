"""
AOIS-HROP Phase 13.7 - Incident Detector
Autonomous detector for timeouts, latency spikes, memory leaks, queue explosions, retry storms, and worker crashes.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from app.runtime.operations.events.operation_events import OperationalSeverity, SubsystemType
from app.runtime.operations.incidents.incident_classifier import IncidentClassifier


@dataclass
class DetectedIncident:
    incident_id: str
    title: str
    subsystem: SubsystemType
    error_type: str
    severity: OperationalSeverity
    detected_at: str
    details: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False


class IncidentDetector:
    """
    Scans live telemetry metrics and thresholds to detect active incidents automatically.
    """

    def __init__(self):
        self.classifier = IncidentClassifier()
        self._detected_incidents: List[DetectedIncident] = []

    def evaluate_telemetry(
        self,
        subsystem: SubsystemType,
        error_rate: float = 0.0,
        latency_p95_ms: float = 200.0,
        memory_utilization_pct: float = 30.0,
        queue_backlog: int = 5,
        retry_count: int = 0,
        affected_missions: int = 1,
    ) -> Optional[DetectedIncident]:
        incident: Optional[DetectedIncident] = None

        if error_rate >= 0.10:
            severity = self.classifier.classify_severity(subsystem, "HIGH_ERROR_RATE", affected_missions)
            incident = self._build_incident(
                title=f"Elevated Error Rate ({round(error_rate * 100, 1)}%) in {subsystem.value}",
                subsystem=subsystem,
                error_type="HIGH_ERROR_RATE",
                severity=severity,
                details={"error_rate": error_rate, "affected_missions": affected_missions},
            )
        elif latency_p95_ms >= 2500.0:
            severity = self.classifier.classify_severity(subsystem, "LATENCY_SPIKE", affected_missions)
            incident = self._build_incident(
                title=f"Severe Latency Spike ({latency_p95_ms}ms) in {subsystem.value}",
                subsystem=subsystem,
                error_type="LATENCY_SPIKE",
                severity=severity,
                details={"latency_p95_ms": latency_p95_ms, "threshold": 2500.0},
            )
        elif memory_utilization_pct >= 90.0:
            severity = self.classifier.classify_severity(subsystem, "MEMORY_LEAK", affected_missions)
            incident = self._build_incident(
                title=f"Near-OOM Memory Saturation ({memory_utilization_pct}%) in {subsystem.value}",
                subsystem=subsystem,
                error_type="MEMORY_LEAK",
                severity=severity,
                details={"memory_utilization_pct": memory_utilization_pct},
            )
        elif queue_backlog >= 100:
            severity = self.classifier.classify_severity(subsystem, "QUEUE_EXPLOSION", affected_missions)
            incident = self._build_incident(
                title=f"Queue Ingestion Backlog Explosion ({queue_backlog} items) in {subsystem.value}",
                subsystem=subsystem,
                error_type="QUEUE_EXPLOSION",
                severity=severity,
                details={"queue_backlog": queue_backlog},
            )
        elif retry_count >= 5:
            severity = self.classifier.classify_severity(subsystem, "RETRY_STORM", affected_missions)
            incident = self._build_incident(
                title=f"Retry Storm Detected ({retry_count} retries) in {subsystem.value}",
                subsystem=subsystem,
                error_type="RETRY_STORM",
                severity=severity,
                details={"retry_count": retry_count},
            )

        return incident

    def _build_incident(
        self,
        title: str,
        subsystem: SubsystemType,
        error_type: str,
        severity: OperationalSeverity,
        details: Dict[str, Any],
    ) -> DetectedIncident:
        inc = DetectedIncident(
            incident_id=f"inc-{uuid.uuid4().hex[:8]}",
            title=title,
            subsystem=subsystem,
            error_type=error_type,
            severity=severity,
            detected_at=datetime.now(timezone.utc).isoformat(),
            details=details,
            resolved=False,
        )
        self._detected_incidents.append(inc)
        return inc

    def get_active_incidents(self) -> List[DetectedIncident]:
        return [i for i in self._detected_incidents if not i.resolved]

    def get_all_incidents(self) -> List[DetectedIncident]:
        return self._detected_incidents
