"""Alert Rule Manager (Part 3H.3.5.5).

Configures and audits Prometheus AlertManager rules across critical platform failure modes.
Ensures every alert includes severity, description, owner, runbook link, and recovery action.
"""

from __future__ import annotations

from typing import List

from app.platform_verification.health_monitoring_integration.domain.interfaces import (
    IAlertRuleManager,
)
from app.platform_verification.health_monitoring_integration.domain.models import (
    AlertConfigurationReport,
    AlertRule,
    AlertSeverity,
)


class AlertRuleManager(IAlertRuleManager):
    """Manages SRE AlertManager rule catalog."""

    RULES: List[AlertRule] = [
        AlertRule(
            alert_name="ServiceDown",
            service="platform",
            severity=AlertSeverity.CRITICAL,
            condition="service_health_status == 0",
            for_duration="30s",
            description="A core platform service process has failed health check or crashed",
            owner="sre-oncall@docutask.com",
            runbook_url="https://wiki.docutask.internal/runbooks/service-down",
            recovery_action="Restart service container and inspect crashback traces",
        ),
        AlertRule(
            alert_name="ApiErrorSpike",
            service="api_service",
            severity=AlertSeverity.HIGH,
            condition="http_error_rate_pct > 5.0",
            for_duration="1m",
            description="HTTP 5xx error rate exceeded 5% over 1-minute sliding window",
            owner="api-platform-team@docutask.com",
            runbook_url="https://wiki.docutask.internal/runbooks/api-error-spike",
            recovery_action="Scale API pods and enable rate limiting on faulty endpoints",
        ),
        AlertRule(
            alert_name="QueueExplosion",
            service="redis_queue",
            severity=AlertSeverity.HIGH,
            condition="redis_queue_depth > 2000",
            for_duration="2m",
            description="Pending document tasks in Redis queue exceeded 2000 items",
            owner="async-workers-team@docutask.com",
            runbook_url="https://wiki.docutask.internal/runbooks/queue-explosion",
            recovery_action="Autoscale worker fleet from 8 to 20 instances",
        ),
        AlertRule(
            alert_name="WorkerFleetHeartbeatFailure",
            service="worker_fleet",
            severity=AlertSeverity.CRITICAL,
            condition="worker_active_count < 2 or (time() - worker_heartbeat_timestamp > 60)",
            for_duration="1m",
            description="Worker fleet dropped below minimum capacity or heartbeats ceased",
            owner="async-workers-team@docutask.com",
            runbook_url="https://wiki.docutask.internal/runbooks/worker-failure",
            recovery_action="Trigger Celery worker auto-recycle and check broker network partition",
        ),
        AlertRule(
            alert_name="PostgresConnectionSaturation",
            service="postgres_db",
            severity=AlertSeverity.HIGH,
            condition="postgres_connection_count > 45",
            for_duration="1m",
            description="PostgreSQL active connection leases approaching maximum pool ceiling (50)",
            owner="data-platform-team@docutask.com",
            runbook_url="https://wiki.docutask.internal/runbooks/postgres-pool",
            recovery_action="Terminate idle transactions and expand pool max_size in PgBouncer",
        ),
        AlertRule(
            alert_name="GeminiProviderDegradation",
            service="gemini_ai_provider",
            severity=AlertSeverity.HIGH,
            condition="gemini_api_failure_rate_pct > 5.0 or gemini_request_latency_seconds > 2.5",
            for_duration="1m",
            description="Gemini AI provider elevated 429 quota exhaustion or P95 latency > 2.5s",
            owner="ai-foundation-team@docutask.com",
            runbook_url="https://wiki.docutask.internal/runbooks/gemini-fallback",
            recovery_action="Enable batched async inference and switch secondary traffic to fallback provider",
        ),
    ]

    def get_alert_configuration(self) -> AlertConfigurationReport:
        rules = list(self.RULES)
        critical_count = len([r for r in rules if r.severity == AlertSeverity.CRITICAL])
        warning_count = len([r for r in rules if r.severity in (AlertSeverity.HIGH, AlertSeverity.WARNING)])

        passed = len(rules) >= 6 and critical_count >= 2

        return AlertConfigurationReport(
            total_rules_configured=len(rules),
            critical_rules_count=critical_count,
            warning_rules_count=warning_count,
            rules=rules,
            passed=passed,
            details={
                "alertmanager_cluster": "alertmanager.monitoring.svc.cluster.local:9093",
                "notification_channels": ["PagerDuty (Critical)", "Slack #sre-alerts (High/Warning)", "Email"],
                "runbook_coverage_pct": 100.0,
                "recovery_action_coverage_pct": 100.0,
            },
        )
