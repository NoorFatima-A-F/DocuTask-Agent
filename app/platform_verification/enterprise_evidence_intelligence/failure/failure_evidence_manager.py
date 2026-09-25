"""
Phase 3P: Failure Evidence & Root Cause Intelligence Manager.
"""

from datetime import datetime, timezone
from typing import List

from ..domain.interfaces import IFailureEvidenceManager
from ..domain.models import (
    EvidenceSeverity,
    EvidenceStatus,
    FailureEvidenceItem,
    FailureEvidenceReport,
    StandardizedEvidenceItem,
)


class FailureEvidenceManager(IFailureEvidenceManager):
    """
    Transforms failed verification checks into structured, actionable failure intelligence
    with root cause diagnosis, operational impact analysis, and remediation steps.
    """

    def analyze_failures(self, items: List[StandardizedEvidenceItem]) -> FailureEvidenceReport:
        failed_items = [it for it in items if it.status in [EvidenceStatus.FAIL, EvidenceStatus.WARN]]
        findings: List[FailureEvidenceItem] = []

        for idx, item in enumerate(failed_items):
            findings.append(
                FailureEvidenceItem(
                    failure_id=f"FAIL-{idx + 1:03d}",
                    failure=f"{item.test_name} failed verification",
                    severity=item.severity,
                    component=item.component,
                    impact=self._determine_impact(item),
                    root_cause=item.details or "Component threshold exceeded or assertion returned false.",
                    recommendation=self._determine_recommendation(item),
                    reproduction_steps=[
                        f"1. Target component: {item.component}",
                        f"2. Trigger test scenario: {item.test_name}",
                        f"3. Evaluate metric response against target envelope",
                    ],
                    timestamp=datetime.now(timezone.utc).isoformat(),
                )
            )

        critical_count = sum(1 for f in findings if f.severity == EvidenceSeverity.CRITICAL)
        high_count = sum(1 for f in findings if f.severity == EvidenceSeverity.HIGH)

        return FailureEvidenceReport(
            failures_detected=len(findings),
            critical_failures_count=critical_count,
            high_failures_count=high_count,
            failures=findings,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    def _determine_impact(self, item: StandardizedEvidenceItem) -> str:
        if item.category == "Reliability":
            return "Potential worker degradation or delayed task processing under failure scenarios."
        if item.category == "Security":
            return "Elevated risk of unauthorized access, secret leakage, or supply-chain compromise."
        if item.category == "Scalability":
            return "Increased P95 latency or queue backlog under peak document ingestion burst."
        if item.category == "Recovery Capability":
            return "Breach of agreed RTO (<15m) or RPO (<5m) disaster recovery SLAs."
        return "Operational variance requiring monitoring attention."

    def _determine_recommendation(self, item: StandardizedEvidenceItem) -> str:
        if item.category == "Reliability":
            return "Adjust exponential backoff parameters and increase worker replica count."
        if item.category == "Security":
            return "Harden IAM policies, rotate credentials via KMS, and rebuild container base image."
        if item.category == "Scalability":
            return "Optimize PostgreSQL index definitions and configure horizontal pod autoscaling threshold."
        if item.category == "Recovery Capability":
            return "Verify asynchronous database replication streaming and test automated failover scripts."
        return "Inspect component telemetry logs and adjust operational configuration."
