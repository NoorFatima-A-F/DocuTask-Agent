"""AI Monitoring Quality Scorer & Certification Engine (Part 3H.3.9.12).

Calculates weighted multi-category scores across AI observability dimensions.
Weights:
- Telemetry completeness: 20%
- Metrics coverage: 20%
- Dashboard quality: 15%
- Logging quality: 15%
- Alert reliability: 15%
- Security: 15%
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.platform_verification.ai_health_monitoring.domain.interfaces import (
    IAIObservabilityQualityScorer,
)
from app.platform_verification.ai_health_monitoring.domain.models import (
    AIAlertingReport,
    AIAutomatedResponseReport,
    AIDashboardReport,
    AIIncidentTestReport,
    AILoggingReport,
    AIMetricsReport,
    AIMonitoringSecurityReport,
    AIObservabilityArchitectureReport,
    AIObservabilityScorecard,
    AIObservabilityTier,
    AISLOReport,
    AITracingReport,
)


class AIMonitoringQualityScorer(IAIObservabilityQualityScorer):
    """Computes weighted multi-factor observability scores and issues enterprise certifications."""

    WEIGHT_TELEMETRY = 0.20
    WEIGHT_METRICS = 0.20
    WEIGHT_DASHBOARDS = 0.15
    WEIGHT_LOGGING = 0.15
    WEIGHT_ALERTS = 0.15
    WEIGHT_SECURITY = 0.15

    TARGET_THRESHOLD = 95.0

    def compute_scorecard(
        self,
        arch_report: AIObservabilityArchitectureReport,
        metrics_report: AIMetricsReport,
        dashboard_report: AIDashboardReport,
        logging_report: AILoggingReport,
        tracing_report: AITracingReport,
        alerting_report: AIAlertingReport,
        slo_report: AISLOReport,
        incident_report: AIIncidentTestReport,
        automation_report: AIAutomatedResponseReport,
        security_report: AIMonitoringSecurityReport,
    ) -> AIObservabilityScorecard:
        # 1. Telemetry Completeness (20%)
        # Evaluates architecture pipelines and distributed tracing
        arch_score = 100.0 if arch_report.passed else 50.0
        trace_score = 100.0 if tracing_report.passed else 50.0
        telemetry_score = round(0.5 * arch_score + 0.5 * trace_score, 2)

        # 2. Metrics Coverage (20%)
        # Evaluates 5-category metric collection and SLO attainment
        metrics_sub = 100.0 if metrics_report.passed else 50.0
        slo_sub = 100.0 if slo_report.passed else 50.0
        metrics_score = round(0.6 * metrics_sub + 0.4 * slo_sub, 2)

        # 3. Dashboard Quality (15%)
        dashboard_score = 100.0 if dashboard_report.passed else 50.0

        # 4. Logging Quality (15%)
        logging_score = 100.0 if logging_report.passed else 50.0

        # 5. Alert Reliability & Automation (15%)
        alert_sub = 100.0 if alerting_report.passed else 50.0
        inc_sub = 100.0 if incident_report.passed else 50.0
        auto_sub = 100.0 if automation_report.passed else 50.0
        alert_score = round(0.4 * alert_sub + 0.3 * inc_sub + 0.3 * auto_sub, 2)

        # 6. Security (15%)
        security_score = 100.0 if (security_report.passed and not security_report.sensitive_data_exposed) else 40.0

        # Overall Composite Score
        overall_score = round(
            (telemetry_score * self.WEIGHT_TELEMETRY)
            + (metrics_score * self.WEIGHT_METRICS)
            + (dashboard_score * self.WEIGHT_DASHBOARDS)
            + (logging_score * self.WEIGHT_LOGGING)
            + (alert_score * self.WEIGHT_ALERTS)
            + (security_score * self.WEIGHT_SECURITY),
            2,
        )

        # Determine Tier
        if overall_score >= 95.0:
            tier = AIObservabilityTier.ENTERPRISE_AI_OBSERVABILITY_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall_score >= 90.0:
            tier = AIObservabilityTier.PRODUCTION_AI_MONITORING_READY
            verdict = "CONDITIONAL_APPROVAL"
            passed = True
        elif overall_score >= 80.0:
            tier = AIObservabilityTier.IMPROVEMENT_REQUIRED
            verdict = "REJECTED_REMEDIATION_REQUIRED"
            passed = False
        else:
            tier = AIObservabilityTier.FAILED
            verdict = "REJECTED"
            passed = False

        return AIObservabilityScorecard(
            telemetry_completeness_score=telemetry_score,
            metrics_coverage_score=metrics_score,
            dashboard_quality_score=dashboard_score,
            logging_quality_score=logging_score,
            alert_reliability_score=alert_score,
            security_score=security_score,
            overall_score=overall_score,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            details={
                "target_threshold_pct": self.TARGET_THRESHOLD,
                "weights": {
                    "telemetry_completeness": self.WEIGHT_TELEMETRY,
                    "metrics_coverage": self.WEIGHT_METRICS,
                    "dashboard_quality": self.WEIGHT_DASHBOARDS,
                    "logging_quality": self.WEIGHT_LOGGING,
                    "alert_reliability": self.WEIGHT_ALERTS,
                    "security": self.WEIGHT_SECURITY,
                },
            },
        )
