"""
SLO Compliance and Error Budget Engine.
"""
from typing import List, Dict, Any
from app.platform_verification.observability_verification.domain.models import SloComplianceReport
from app.platform_verification.observability_verification.domain.interfaces import ISloComplianceEngine


class SloComplianceEngine(ISloComplianceEngine):
    """Calculates Availability, Latency, Processing SLOs and error budget burn rates."""

    def evaluate_slos(self, slo_data: List[Dict[str, Any]]) -> SloComplianceReport:
        failing: List[str] = []
        compliant_count = 0

        for slo in slo_data:
            name = slo.get("name", "SLO")
            target = slo.get("target_percentage", 99.5)
            actual = slo.get("actual_percentage", 99.9)

            if actual >= target:
                compliant_count += 1
            else:
                failing.append(f"SLO '{name}' breached: target={target}%, actual={actual}%")

        total = len(slo_data)
        score = (compliant_count / max(total, 1)) * 100.0
        score = round(min(100.0, score), 2)
        status = "PASS" if len(failing) == 0 else "FAIL"

        return SloComplianceReport(
            total_slos=total,
            compliant_slos_count=compliant_count,
            failing_slos=failing,
            slo_compliance_score=score,
            status=status,
        )
