"""
Pyramid Verification Dashboard generating maturity distribution, coverage, and risk metrics.
"""
from __future__ import annotations
from typing import Dict, List
from app.platform_verification.pyramid_engine.domain.models import (
    ComponentCoverageItem,
    DefectRecord,
    PyramidExecutionReport,
    PyramidDashboardSummary,
    FailureSeverity,
    VerificationLevel,
)
from app.platform_verification.pyramid_engine.domain.interfaces import IPyramidDashboard


class PyramidDashboard(IPyramidDashboard):
    """Calculates platform-wide verification maturity, quality trends, and risk index."""

    def generate_summary(
        self,
        components: List[ComponentCoverageItem],
        defects: List[DefectRecord],
        reports: List[PyramidExecutionReport],
    ) -> PyramidDashboardSummary:
        total_comp = len(components)
        verified_comp = sum(1 for c in components if c.is_verified)
        unverified_comp = total_comp - verified_comp
        cov_pct = (verified_comp / total_comp * 100.0) if total_comp > 0 else 0.0

        # Maturity distribution across L0 - L7
        dist: Dict[str, int] = {lvl.value: 0 for lvl in VerificationLevel}
        for c in components:
            dist[c.current_level.value] = dist.get(c.current_level.value, 0) + 1

        # Defect distribution by severity
        open_defects: Dict[str, int] = {
            FailureSeverity.CRITICAL.value: 0,
            FailureSeverity.HIGH.value: 0,
            FailureSeverity.MEDIUM.value: 0,
            FailureSeverity.LOW.value: 0,
        }
        for d in defects:
            if d.status == "OPEN":
                open_defects[d.severity.value] = open_defects.get(d.severity.value, 0) + 1

        # Overall pass rate across recent reports
        if reports:
            total_t = sum(sum(s.total_tests for s in r.level_summaries.values()) for r in reports)
            passed_t = sum(sum(s.passed_tests for s in r.level_summaries.values()) for r in reports)
            overall_pass = (passed_t / total_t * 100.0) if total_t > 0 else 100.0
        else:
            overall_pass = 100.0

        # Risk index: weighted sum of open defects and unverified components
        crit_count = open_defects[FailureSeverity.CRITICAL.value]
        high_count = open_defects[FailureSeverity.HIGH.value]
        med_count = open_defects[FailureSeverity.MEDIUM.value]
        unverified_ratio = (unverified_comp / max(1, total_comp))

        raw_risk = (crit_count * 30.0) + (high_count * 15.0) + (med_count * 5.0) + (unverified_ratio * 40.0)
        risk_index = round(min(100.0, raw_risk), 2)

        return PyramidDashboardSummary(
            total_components=total_comp,
            verified_components=verified_comp,
            unverified_components=unverified_comp,
            coverage_pct=round(cov_pct, 2),
            overall_pass_rate=round(overall_pass, 2),
            maturity_distribution=dist,
            open_defects_by_severity=open_defects,
            risk_index=risk_index,
        )
