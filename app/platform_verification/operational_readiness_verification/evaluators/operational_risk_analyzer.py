"""
Phase 3H.4.11.10: Operational Risk Analyzer Engine
"""
from typing import List
from ..domain.interfaces import IOperationalRiskAnalyzer
from ..domain.models import (
    OperationalRiskReport,
    RiskItem,
    RiskLevel,
    MetricsCompletenessScore,
    MonitoringAccuracyScore,
    AlertReliabilityScore,
    IncidentQualityScore,
    DashboardUsabilityScore,
    SecurityReadinessScore,
)


class OperationalRiskAnalyzer(IOperationalRiskAnalyzer):
    def analyze_operational_risks(
        self,
        metrics_score: MetricsCompletenessScore,
        monitoring_score: MonitoringAccuracyScore,
        alert_score: AlertReliabilityScore,
        incident_score: IncidentQualityScore,
        dashboard_score: DashboardUsabilityScore,
        security_score: SecurityReadinessScore,
    ) -> OperationalRiskReport:
        risks: List[RiskItem] = []

        # Hard-Gate Rule 1: Security Readiness < 70% is a critical release blocker
        if security_score.score < 70.0:
            risks.append(
                RiskItem(
                    risk_id="RISK-CRIT-SEC",
                    category="Security",
                    severity=RiskLevel.CRITICAL,
                    description=f"Observability security controls score ({security_score.score}%) is below 70.0% threshold. Production deployment blocked.",
                    is_blocking=True,
                    remediation_ref="REM-SEC-001",
                )
            )

        # Hard-Gate Rule 2: Alert Reliability < 75% triggers high operational risk
        if alert_score.score < 75.0:
            risks.append(
                RiskItem(
                    risk_id="RISK-HIGH-ALERT",
                    category="Alerting",
                    severity=RiskLevel.HIGH,
                    description=f"Alert reliability score ({alert_score.score}%) is below 75.0% threshold.",
                    is_blocking=True,
                    remediation_ref="REM-ALERT-001",
                )
            )

        # Rule 3: Monitoring accuracy latency
        if not monitoring_score.mttd_benchmark_met:
            risks.append(
                RiskItem(
                    risk_id="RISK-MED-LATENCY",
                    category="Detection",
                    severity=RiskLevel.MEDIUM,
                    description=f"Mean time to detect ({monitoring_score.mean_time_to_detect_seconds}s) exceeds 30.0s SLA.",
                    is_blocking=False,
                    remediation_ref="REM-DET-001",
                )
            )

        blocking_count = sum(1 for r in risks if r.is_blocking)
        if blocking_count > 0:
            overall_risk = RiskLevel.HIGH if any(r.severity == RiskLevel.HIGH for r in risks) else RiskLevel.CRITICAL
        elif len(risks) > 0:
            overall_risk = RiskLevel.MEDIUM
        else:
            overall_risk = RiskLevel.NEGLIGIBLE

        return OperationalRiskReport(
            overall_risk=overall_risk,
            blocking_risks_count=blocking_count,
            hard_gate_passed=(blocking_count == 0),
            evaluated_risks=risks,
        )
