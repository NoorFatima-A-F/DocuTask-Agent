"""
AOIS-HROP Phase 13.7 - Incident Classifier
Classifies incident severity based on blast radius, error criticality, and SLA impact.
"""

from app.runtime.operations.events.operation_events import OperationalSeverity, SubsystemType


class IncidentClassifier:
    """
    Evaluates incident attributes to assign standardized severity ratings.
    """

    def classify_severity(
        self,
        subsystem: SubsystemType,
        error_type: str,
        affected_missions_count: int = 1,
        is_data_loss_risk: bool = False,
        is_sla_breached: bool = False,
    ) -> OperationalSeverity:
        if is_data_loss_risk or (is_sla_breached and affected_missions_count > 5):
            return OperationalSeverity.CRITICAL

        if subsystem in (SubsystemType.PLANNER, SubsystemType.TRUTH, SubsystemType.DATABASE) and affected_missions_count > 1:
            return OperationalSeverity.HIGH

        if error_type in ("RETRY_STORM", "DEADLOCK", "MEMORY_LEAK", "MODEL_RATE_LIMIT"):
            return OperationalSeverity.HIGH if affected_missions_count > 3 else OperationalSeverity.MEDIUM

        if affected_missions_count > 1:
            return OperationalSeverity.MEDIUM

        return OperationalSeverity.LOW
