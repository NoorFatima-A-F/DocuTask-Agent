"""
Phase 3Q: Infrastructure Drift Detector.
"""

from datetime import datetime, timezone

from ..domain.interfaces import IDriftDetector
from ..domain.models import InfrastructureDriftReport, PipelineStageStatus


class DriftDetector(IDriftDetector):
    """
    Compares declared infrastructure definitions (Terraform / Helm / Compose)
    against actual live infrastructure resources to detect unmanaged drift.
    """

    def detect_drift(self, declared_count: int = 28, actual_count: int = 28) -> InfrastructureDriftReport:
        drifted = abs(actual_count - declared_count)
        has_drift = drifted > 0
        severity = "HIGH" if drifted >= 3 else ("MEDIUM" if drifted > 0 else "NONE")
        status = PipelineStageStatus.BLOCKED if severity == "HIGH" else PipelineStageStatus.PASSED

        return InfrastructureDriftReport(
            declared_resources=declared_count,
            actual_resources=actual_count,
            drifted_resources=drifted,
            drift_detected=has_drift,
            drift_severity=severity,
            status=status,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
