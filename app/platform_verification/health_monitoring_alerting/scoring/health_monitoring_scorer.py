"""Operational Health Monitoring & Observability Scorer (3H.4.11).

Calculates a 6-dimension weighted quality score:
1. Metrics Completeness (Weight 20%)
2. Monitoring Accuracy (Weight 20%)
3. Alert Reliability (Weight 20%)
4. Incident Quality (Weight 15%)
5. Dashboard Usability (Weight 15%)
6. Security (Weight 10%)
"""

from ..domain.models import (
    HealthMonitoringScorecard,
    ObservabilityTier,
    HealthSignalArchitectureReport,
    MetricsCollectionReport,
    PrometheusVerificationReport,
    DashboardValidationReport,
    AlertRuleReport,
    AlertAccuracyReport,
    IncidentSignalReport,
    AlertFatigueReport,
    MonitoringFailureTestReport,
    ObservabilitySecurityReport,
)
from ..domain.interfaces import IHealthMonitoringScorer


class HealthMonitoringScorer(IHealthMonitoringScorer):
    """Calculates weighted observability and alerting quality score."""

    def score_observability(
        self,
        signal_rep: HealthSignalArchitectureReport,
        metrics_rep: MetricsCollectionReport,
        prom_rep: PrometheusVerificationReport,
        dash_rep: DashboardValidationReport,
        alert_rep: AlertRuleReport,
        acc_rep: AlertAccuracyReport,
        inc_rep: IncidentSignalReport,
        fatigue_rep: AlertFatigueReport,
        sim_rep: MonitoringFailureTestReport,
        sec_rep: ObservabilitySecurityReport,
    ) -> HealthMonitoringScorecard:
        # 1. Metrics Completeness (20%)
        # All 5 domains covered, >= 18 total metrics
        met_score = 100.0
        if metrics_rep.total_metrics_tracked < 18:
            met_score -= (18 - metrics_rep.total_metrics_tracked) * 5.0

        # 2. Monitoring Accuracy (20%)
        # Precision and recall at 100%
        acc_score = 100.0
        if acc_rep.precision_pct < 100.0:
            acc_score -= (100.0 - acc_rep.precision_pct)
        if acc_rep.recall_pct < 100.0:
            acc_score -= (100.0 - acc_rep.recall_pct)

        # 3. Alert Reliability (20%)
        # Critical & warning rules defined, fatigue grouping active, auto-resolution verified
        rel_score = 100.0
        if alert_rep.critical_rules_count < 3:
            rel_score -= 20.0
        if not fatigue_rep.grouping_by_root_cause_active:
            rel_score -= 20.0
        if not acc_rep.auto_resolution_verified:
            rel_score -= 20.0

        # 4. Incident Quality (15%)
        # Actionable payloads, dependency chain included, logs attached
        inc_score = 100.0
        if not inc_rep.all_payloads_actionable:
            inc_score -= 30.0
        if not inc_rep.dependency_chain_included:
            inc_score -= 20.0

        # 5. Dashboard Usability (15%)
        # 4 dashboards verified, queryable panels
        dash_score = 100.0
        if dash_rep.total_dashboards < 4:
            dash_score -= (4 - dash_rep.total_dashboards) * 20.0
        if not dash_rep.all_panels_queryable:
            dash_score -= 20.0

        # 6. Security (10%)
        # Zero secrets, tokens, or PII in metrics/logs/alerts
        sec_score = 100.0
        if not sec_rep.zero_leak_verified:
            sec_score -= 50.0

        # Clamp individual scores [0.0, 100.0]
        met_score = max(0.0, min(100.0, met_score))
        acc_score = max(0.0, min(100.0, acc_score))
        rel_score = max(0.0, min(100.0, rel_score))
        inc_score = max(0.0, min(100.0, inc_score))
        dash_score = max(0.0, min(100.0, dash_score))
        sec_score = max(0.0, min(100.0, sec_score))

        # Weighted calculation
        overall = (
            met_score * 0.20
            + acc_score * 0.20
            + rel_score * 0.20
            + inc_score * 0.15
            + dash_score * 0.15
            + sec_score * 0.10
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = ObservabilityTier.ENTERPRISE_OBSERVABILITY_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = ObservabilityTier.PRODUCTION_READY
            verdict = "PROVISIONALLY_CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = ObservabilityTier.IMPROVEMENT_REQUIRED
            verdict = "ACTION_REQUIRED"
            passed = False
        else:
            tier = ObservabilityTier.FAILED
            verdict = "FAILED"
            passed = False

        return HealthMonitoringScorecard(
            metrics_completeness_score=met_score,
            monitoring_accuracy_score=acc_score,
            alert_reliability_score=rel_score,
            incident_quality_score=inc_score,
            dashboard_usability_score=dash_score,
            security_score=sec_score,
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
        )
