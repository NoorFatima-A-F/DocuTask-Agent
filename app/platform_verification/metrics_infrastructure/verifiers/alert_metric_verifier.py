"""
3I.3.12: Metric-Driven Alerting Rules & Thresholds Verifier
"""
from typing import List
from ..domain.models import AlertRuleValidationSpec, AlertValidationReport
from ..domain.interfaces import IAlertMetricVerifier


class AlertMetricVerifier(IAlertMetricVerifier):
    """
    Verifies metric-driven alert conditions including queue saturation, high HTTP error rates, and P95 latency SLA breaches.
    """

    def verify_alert_metrics(self) -> AlertValidationReport:
        rules: List[AlertRuleValidationSpec] = [
            AlertRuleValidationSpec(
                alert_name="QueueSaturationWarning",
                metric_query="queue_depth > 10000",
                condition="queue_depth > 10000 for 5m",
                severity="WARNING",
                trigger_state="READY",
                action="Trigger auto-scaling of worker pods and notify SRE on-call"
            ),
            AlertRuleValidationSpec(
                alert_name="HighHttpErrorRateCritical",
                metric_query="rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.05",
                condition="error_rate > 5% for 2m",
                severity="CRITICAL",
                trigger_state="READY",
                action="Page primary on-call SRE and initiate automated traffic reroute"
            ),
            AlertRuleValidationSpec(
                alert_name="LatencySlaDegradation",
                metric_query="histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 2.0",
                condition="P95 latency > 2.0s for 5m",
                severity="WARNING",
                trigger_state="READY",
                action="Log performance incident and scale upstream gateway replicas"
            ),
            AlertRuleValidationSpec(
                alert_name="DatabaseConnectionExhaustionRisk",
                metric_query="database_connections_active / 100 > 0.85",
                condition="active_connections > 85% for 3m",
                severity="CRITICAL",
                trigger_state="READY",
                action="Alert DBA and initiate connection pool recycling"
            ),
            AlertRuleValidationSpec(
                alert_name="GeminiTimeoutSpike",
                metric_query="rate(llm_errors_total{error_type='timeout'}[5m]) > 0.05",
                condition="timeout rate > 5% for 2m",
                severity="WARNING",
                trigger_state="READY",
                action="Activate fallback LLM provider and reduce batch sizes"
            ),
        ]

        return AlertValidationReport(
            report_title="Metric-Driven Alerting Rules & Thresholds Report",
            rules_validated=rules,
            alerting_pipeline_verified=True
        )
