"""
AOIS-HROP Phase 13.7 - Incident Impact Analyzer
Quantifies business impact, affected missions, users, SLA breaches, and financial risk exposure.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class IncidentImpactReport:
    incident_id: str
    affected_missions_count: int
    affected_users_count: int
    sla_breach_occurred: bool
    estimated_financial_loss_usd: float
    reputation_risk_level: str  # LOW, MODERATE, HIGH, CRITICAL


class IncidentImpactAnalyzer:
    """
    Computes tangible business and technical cost associated with runtime incidents.
    """

    def analyze_impact(
        self,
        incident_id: str,
        affected_missions: List[str],
        duration_seconds: float,
        severity: str,
        sla_threshold_seconds: float = 5.0,
    ) -> IncidentImpactReport:
        count = len(affected_missions)
        users = max(1, count * 2)

        sla_breach = duration_seconds > sla_threshold_seconds
        # Base financial loss calculation: $0.15 per mission + penalty per second late
        base_cost = count * 0.15
        late_penalty = max(0.0, (duration_seconds - sla_threshold_seconds) * 0.05 * count) if sla_breach else 0.0
        total_loss = round(base_cost + late_penalty, 4)

        if severity == "CRITICAL" or total_loss > 10.0:
            reputation = "CRITICAL"
        elif severity == "HIGH" or total_loss > 2.0:
            reputation = "HIGH"
        elif total_loss > 0.5:
            reputation = "MODERATE"
        else:
            reputation = "LOW"

        return IncidentImpactReport(
            incident_id=incident_id,
            affected_missions_count=count,
            affected_users_count=users,
            sla_breach_occurred=sla_breach,
            estimated_financial_loss_usd=total_loss,
            reputation_risk_level=reputation,
        )
