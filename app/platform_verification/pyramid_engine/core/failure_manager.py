"""
Failure Management, Root Cause Analysis, and Defect Creation.
"""
from __future__ import annotations
import uuid
from typing import Dict, List, Optional
from app.platform_verification.pyramid_engine.domain.models import (
    TestExecutionRecord,
    DefectRecord,
    FailureSeverity,
    TestClassification,
)
from app.platform_verification.pyramid_engine.domain.interfaces import IFailureClassifier


class FailureManager(IFailureClassifier):
    """Detects, classifies, and tracks verification failures."""

    def __init__(self) -> None:
        self._defects: Dict[str, DefectRecord] = {}

    def classify_failure(self, test_record: TestExecutionRecord) -> DefectRecord:
        msg = (test_record.error_message or "").lower()
        test_name = test_record.name.lower()

        # Automatic Severity Classification
        if any(term in msg or term in test_name for term in ["security", "injection", "leak", "corruption", "crash", "auth"]):
            severity = FailureSeverity.CRITICAL
            root_cause = "Security vulnerability or critical system integrity violation."
        elif any(term in msg or term in test_name for term in ["workflow", "extraction", "accuracy", "hallucination", "timeout"]):
            severity = FailureSeverity.HIGH
            root_cause = "Workflow orchestration failure or AI accuracy degradation."
        elif any(term in msg or term in test_name for term in ["latency", "slow", "performance", "memory"]):
            severity = FailureSeverity.MEDIUM
            root_cause = "Resource bottleneck or performance degradation."
        else:
            severity = FailureSeverity.LOW
            root_cause = "Minor behavioral discrepancy or logging failure."

        defect = DefectRecord(
            bug_id=f"BUG-{uuid.uuid4().hex[:6].upper()}",
            title=f"Verification Failure in {test_record.name}",
            original_failure=test_record.error_message or "Unknown failure",
            component=test_record.name.split("_")[0] if "_" in test_record.name else "platform_core",
            severity=severity,
            detected_at_level=test_record.level,
            root_cause=root_cause,
        )

        self._defects[defect.bug_id] = defect
        return defect

    def get_defect(self, bug_id: str) -> Optional[DefectRecord]:
        return self._defects.get(bug_id)

    def list_defects(self) -> List[DefectRecord]:
        return list(self._defects.values())
