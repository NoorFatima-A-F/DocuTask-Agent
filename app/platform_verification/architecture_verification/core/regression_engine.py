"""
Architecture Regression Detection Engine comparing baseline and current scans.
"""
from __future__ import annotations
from typing import List
from app.platform_verification.architecture_verification.domain.interfaces import IArchitectureRegressionEngine
from app.platform_verification.architecture_verification.domain.models import (
    ArchitectureEvidencePackage,
    ArchitectureRegressionReport,
    ArchitectureViolation,
)


class EnterpriseArchitectureRegressionEngine(IArchitectureRegressionEngine):
    """Detects score degradation, new critical violations, or new circular dependencies."""

    def detect_regression(
        self,
        baseline_evidence: ArchitectureEvidencePackage,
        current_evidence: ArchitectureEvidencePackage,
    ) -> ArchitectureRegressionReport:
        score_delta = round(
            current_evidence.score_report.total_score - baseline_evidence.score_report.total_score, 2
        )

        baseline_violation_ids = {v.rule_id + v.source_file for v in baseline_evidence.violations}
        new_violations: List[ArchitectureViolation] = [
            v for v in current_evidence.violations
            if (v.rule_id + v.source_file) not in baseline_violation_ids
        ]

        resolved_count = max(0, len(baseline_evidence.violations) - len(current_evidence.violations))
        new_deps_count = max(0, len(current_evidence.dependency_graph) - len(baseline_evidence.dependency_graph))

        is_regression = False
        blocking_reason = None

        if score_delta < -3.0:
            is_regression = True
            blocking_reason = f"Architecture score dropped significantly by {score_delta} points."
        elif current_evidence.score_report.critical_violations_count > baseline_evidence.score_report.critical_violations_count:
            is_regression = True
            blocking_reason = "New critical architectural violations introduced."
        elif current_evidence.score_report.circular_dependencies_count > baseline_evidence.score_report.circular_dependencies_count:
            is_regression = True
            blocking_reason = "New circular dependencies introduced."

        return ArchitectureRegressionReport(
            baseline_scan_id=baseline_evidence.scan_id,
            current_scan_id=current_evidence.scan_id,
            score_delta=score_delta,
            new_violations=new_violations,
            resolved_violations_count=resolved_count,
            new_dependencies_count=new_deps_count,
            is_regression=is_regression,
            blocking_reason=blocking_reason,
        )
