"""Monitoring Quality Scorer (Part 3H.3.5.12).

Computes weighted quality scorecards across the 6 core health monitoring dimensions:
1. Metric Coverage: 20%
2. Alert Accuracy: 20%
3. Dashboard Quality: 15%
4. Trace Visibility: 15%
5. Incident Diagnosis: 15%
6. Security: 15%
"""

from __future__ import annotations

from typing import Any, Dict

from app.platform_verification.health_monitoring_integration.domain.interfaces import (
    IMonitoringQualityScorer,
)
from app.platform_verification.health_monitoring_integration.domain.models import (
    AlertConfigurationReport,
    AlertQualityReport,
    FailureSimulationReport,
    GrafanaDashboardReport,
    HealthMetricsInventoryReport,
    IncidentVisibilityReport,
    MonitoringQualityScorecard,
    MonitoringSecurityReport,
    ObservabilityArchitectureReport,
    ObservabilityTier,
    PrometheusVerificationReport,
    TracingVerificationReport,
)


class MonitoringQualityScorer(IMonitoringQualityScorer):
    """Calculates composite quality scorecards for health monitoring verification."""

    def compute_scorecard(
        self,
        arch_report: ObservabilityArchitectureReport,
        metrics_report: HealthMetricsInventoryReport,
        prom_report: PrometheusVerificationReport,
        grafana_report: GrafanaDashboardReport,
        alert_config_report: AlertConfigurationReport,
        alert_quality_report: AlertQualityReport,
        incident_report: IncidentVisibilityReport,
        simulation_report: FailureSimulationReport,
        tracing_report: TracingVerificationReport,
        security_report: MonitoringSecurityReport,
    ) -> MonitoringQualityScorecard:
        # 1. Metric Coverage (20%)
        # 8 services covered, >= 25 metrics cataloged, Prometheus scrape successful
        metric_pts = 0.0
        if metrics_report.passed and len(metrics_report.categories_covered) >= 8:
            metric_pts += 50.0
        if prom_report.scrape_successful and prom_report.endpoint_exposed:
            metric_pts += 50.0
        metric_score = min(100.0, metric_pts)

        # 2. Alert Accuracy (20%)
        # Rules configured, precision >= 95%, FPR <= 5%, no noise
        alert_pts = 0.0
        if alert_config_report.passed and alert_config_report.total_rules_configured >= 6:
            alert_pts += 50.0
        if alert_quality_report.benchmarks_met and alert_quality_report.passed:
            alert_pts += 50.0
        alert_score = min(100.0, alert_pts)

        # 3. Dashboard Quality (15%)
        # 4 validated dashboards with valid panels
        dash_pts = 0.0
        if grafana_report.passed and grafana_report.total_dashboards == 4:
            dash_pts += 50.0
        if grafana_report.outage_tested and all(d.valid for d in grafana_report.dashboards_validated):
            dash_pts += 50.0
        dash_score = min(100.0, dash_pts)

        # 4. Trace Visibility (15%)
        # End-to-end 8 spans, context propagated, no missing spans
        trace_pts = 0.0
        if tracing_report.propagation_verified and tracing_report.correlation_ids_valid:
            trace_pts += 50.0
        if tracing_report.passed and tracing_report.span_accuracy_pct >= 95.0:
            trace_pts += 50.0
        trace_score = min(100.0, trace_pts)

        # 5. Incident Diagnosis (15%)
        # Multi-signal cross-correlation, recovery verified, simulations passed
        inc_pts = 0.0
        if incident_report.correlation_complete and incident_report.diagnosis.recovery_verified:
            inc_pts += 50.0
        if simulation_report.passed and simulation_report.total_scenarios_run >= 4:
            inc_pts += 50.0
        inc_score = min(100.0, inc_pts)

        # 6. Security (15%)
        # Zero secrets leaked, redaction active, auth enforced
        sec_pts = 0.0
        if security_report.passed and not security_report.secrets_leaked:
            sec_pts += 50.0
        if security_report.redaction_verified and security_report.auth_enforced:
            sec_pts += 50.0
        sec_score = min(100.0, sec_pts)

        # Weighted calculation
        overall = (
            (metric_score * 0.20)
            + (alert_score * 0.20)
            + (dash_score * 0.15)
            + (trace_score * 0.15)
            + (inc_score * 0.15)
            + (sec_score * 0.15)
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = ObservabilityTier.ENTERPRISE_OBSERVABILITY_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = ObservabilityTier.PRODUCTION_MONITORING_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = ObservabilityTier.NEEDS_IMPROVEMENT
            verdict = "REJECTED"
            passed = False
        else:
            tier = ObservabilityTier.FAILED
            verdict = "REJECTED"
            passed = False

        return MonitoringQualityScorecard(
            metric_coverage_score=round(metric_score, 2),
            alert_accuracy_score=round(alert_score, 2),
            dashboard_quality_score=round(dash_score, 2),
            trace_visibility_score=round(trace_score, 2),
            incident_diagnosis_score=round(inc_score, 2),
            security_score=round(sec_score, 2),
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            details={
                "weights": {
                    "metric_coverage": 0.20,
                    "alert_accuracy": 0.20,
                    "dashboard_quality": 0.15,
                    "trace_visibility": 0.15,
                    "incident_diagnosis": 0.15,
                    "security": 0.15,
                },
                "minimum_required_for_enterprise": 95.0,
            },
        )
