"""GitOps Drift Detection and Policy Enforcement (Req 28, 29)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict


class DriftClassification(str, Enum):
    """Types of infrastructure state drift (Req 28)."""
    EXPECTED_DRIFT = "EXPECTED_DRIFT"
    UNAUTHORIZED_DRIFT = "UNAUTHORIZED_DRIFT"
    EMERGENCY_CHANGE = "EMERGENCY_CHANGE"
    UNKNOWN_DRIFT = "UNKNOWN_DRIFT"


class DriftPolicyAction(str, Enum):
    """Remediation actions triggered by detected drift (Req 29)."""
    REPORT = "REPORT"
    RECONCILE = "RECONCILE"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    QUARANTINE = "QUARANTINE"
    ROLLBACK = "ROLLBACK"


@dataclass
class DriftReport:
    """Detailed drift detection analysis."""
    environment: str
    component: str
    has_drift: bool
    desired_version: str
    actual_version: str
    classification: DriftClassification
    recommended_action: DriftPolicyAction
    differences: Dict[str, Any] = field(default_factory=dict)
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class DriftDetector:
    """Compares desired Git state against live cluster state."""

    @classmethod
    def detect_drift(
        self,
        environment: str,
        component: str,
        desired_state: Dict[str, Any],
        actual_state: Dict[str, Any],
        is_emergency_window: bool = False,
    ) -> DriftReport:
        desired_v = desired_state.get("version", "unknown")
        actual_v = actual_state.get("version", "unknown")

        has_drift = desired_state != actual_state
        differences = {}

        if has_drift:
            for k, v in desired_state.items():
                if actual_state.get(k) != v:
                    differences[k] = {"desired": v, "actual": actual_state.get(k)}

        # Classify drift
        if not has_drift:
            classification = DriftClassification.EXPECTED_DRIFT
            action = DriftPolicyAction.REPORT
        elif is_emergency_window:
            classification = DriftClassification.EMERGENCY_CHANGE
            action = DriftPolicyAction.REQUIRE_APPROVAL
        elif actual_v != desired_v:
            classification = DriftClassification.UNAUTHORIZED_DRIFT
            action = DriftPolicyAction.RECONCILE
        else:
            classification = DriftClassification.UNKNOWN_DRIFT
            action = DriftPolicyAction.REPORT

        return DriftReport(
            environment=environment,
            component=component,
            has_drift=has_drift,
            desired_version=desired_v,
            actual_version=actual_v,
            classification=classification,
            recommended_action=action,
            differences=differences,
        )
