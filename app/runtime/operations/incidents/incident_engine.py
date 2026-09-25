"""
AOIS-HROP Phase 13.7 - Incident Engine
Master incident lifecycle coordinator managing detection, classification, correlation, impact, and timelines.
"""

from typing import Any, Dict, List, Optional
from app.runtime.operations.incidents.incident_classifier import IncidentClassifier
from app.runtime.operations.incidents.incident_detector import IncidentDetector
from app.runtime.operations.incidents.incident_timeline import IncidentTimelineBuilder
from app.runtime.operations.incidents.incident_correlation import IncidentCorrelationEngine
from app.runtime.operations.incidents.incident_impact import IncidentImpactAnalyzer
from app.runtime.operations.events.operation_events import SubsystemType


class IncidentEngine:
    """
    Master coordinator for platform incident detection, classification, correlation, and impact analysis.
    """

    def __init__(self):
        self.classifier = IncidentClassifier()
        self.detector = IncidentDetector()
        self.timeline_builder = IncidentTimelineBuilder()
        self.correlation_engine = IncidentCorrelationEngine()
        self.impact_analyzer = IncidentImpactAnalyzer()

    def record_or_detect_incident(
        self,
        subsystem: SubsystemType,
        error_rate: float = 0.0,
        latency_p95_ms: float = 200.0,
        memory_utilization_pct: float = 30.0,
        queue_backlog: int = 5,
        retry_count: int = 0,
        affected_missions: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        missions = affected_missions or ["mission-default-01"]
        detected = self.detector.evaluate_telemetry(
            subsystem=subsystem,
            error_rate=error_rate,
            latency_p95_ms=latency_p95_ms,
            memory_utilization_pct=memory_utilization_pct,
            queue_backlog=queue_backlog,
            retry_count=retry_count,
            affected_missions=len(missions),
        )

        if not detected:
            return None

        # Build initial timeline entry
        self.timeline_builder.add_entry(
            incident_id=detected.incident_id,
            phase="DETECTED",
            description=f"Automated sensor triggered: {detected.title}",
        )

        impact = self.impact_analyzer.analyze_impact(
            incident_id=detected.incident_id,
            affected_missions=missions,
            duration_seconds=1.5,
            severity=detected.severity.value,
        )

        return {
            "incident_id": detected.incident_id,
            "title": detected.title,
            "subsystem": detected.subsystem.value,
            "error_type": detected.error_type,
            "severity": detected.severity.value,
            "detected_at": detected.detected_at,
            "impact": {
                "affected_missions": impact.affected_missions_count,
                "affected_users": impact.affected_users_count,
                "sla_breach": impact.sla_breach_occurred,
                "financial_loss_usd": impact.estimated_financial_loss_usd,
                "reputation_risk": impact.reputation_risk_level,
            },
            "timeline": [
                {
                    "timestamp": t.timestamp_utc,
                    "phase": t.phase,
                    "description": t.description,
                    "actor": t.actor,
                }
                for t in self.timeline_builder.get_timeline(detected.incident_id)
            ],
        }

    def get_all_incidents_summary(self) -> List[Dict[str, Any]]:
        incidents = self.detector.get_all_incidents()
        return [
            {
                "incident_id": inc.incident_id,
                "title": inc.title,
                "subsystem": inc.subsystem.value,
                "severity": inc.severity.value,
                "detected_at": inc.detected_at,
                "resolved": inc.resolved,
                "details": inc.details,
            }
            for inc in incidents
        ]

    def resolve_incident(self, incident_id: str, summary: str = "Resolved by self-healing action"):
        for inc in self.detector.get_all_incidents():
            if inc.incident_id == incident_id:
                inc.resolved = True
                self.timeline_builder.add_entry(
                    incident_id=incident_id,
                    phase="RESOLVED",
                    description=summary,
                )


_GLOBAL_INCIDENT_ENGINE: Optional[IncidentEngine] = None


def get_incident_engine() -> IncidentEngine:
    global _GLOBAL_INCIDENT_ENGINE
    if _GLOBAL_INCIDENT_ENGINE is None:
        _GLOBAL_INCIDENT_ENGINE = IncidentEngine()
    return _GLOBAL_INCIDENT_ENGINE
