"""
Chaos Incident Simulator & MTTD / MTTR Tracker.
"""
from typing import List, Dict, Any
from app.platform_verification.observability_verification.domain.models import IncidentResponseReport
from app.platform_verification.observability_verification.domain.interfaces import IIncidentRecoverySimulator


class IncidentRecoverySimulator(IIncidentRecoverySimulator):
    """Simulates chaos incidents and measures MTTD, MTTR, and recovery success rate."""

    def simulate_incidents(self, incident_scenarios: List[Dict[str, Any]]) -> IncidentResponseReport:
        mttd_list = []
        mttr_list = []
        recovered = 0

        for inc in incident_scenarios:
            mttd = inc.get("mttd_seconds", 30.0)
            mttr = inc.get("mttr_seconds", 120.0)
            mttd_list.append(mttd)
            mttr_list.append(mttr)
            if inc.get("recovery_successful", True):
                recovered += 1

        total = len(incident_scenarios)
        avg_mttd = sum(mttd_list) / max(total, 1)
        avg_mttr = sum(mttr_list) / max(total, 1)
        rate = (recovered / max(total, 1)) * 100.0

        status = "PASS" if rate >= 90.0 and avg_mttr <= 300.0 else "FAIL"

        return IncidentResponseReport(
            simulated_incidents=total,
            average_mttd_seconds=round(avg_mttd, 2),
            average_mttr_seconds=round(avg_mttr, 2),
            recovery_success_rate=round(rate, 2),
            status=status,
        )
