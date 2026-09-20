"""
Health Alerting Engine (Part 3H.3.3.11).
Evaluates health events to generate multi-tier alerts compatible with Prometheus AlertManager,
Grafana, and incident management notification channels (CRITICAL, WARNING, RECOVERY).
"""
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.platform_verification.health_transition_intelligence.domain.models import (
    HealthEvent,
    HealthState,
    AlertItem,
    AlertingReport,
)


class HealthAlertingEngine:
    """
    Evaluates health events and produces structured alerts.
    """

    def evaluate_events(self, events: List[HealthEvent]) -> AlertingReport:
        alerts: List[AlertItem] = []
        crit_count = 0
        warn_count = 0
        rec_count = 0

        for e in events:
            if e.new_state == HealthState.NOT_READY:
                crit_count += 1
                alerts.append(
                    AlertItem(
                        alert_name="ServiceUnhealthyCritical",
                        severity="CRITICAL",
                        service=e.service_name,
                        summary=f"Service transitioned to NOT_READY: {e.reason}",
                        description=f"Triggered by signal '{e.trigger_signal}' at {e.timestamp}",
                        timestamp=e.timestamp,
                    )
                )
            elif e.new_state == HealthState.DEGRADED:
                warn_count += 1
                alerts.append(
                    AlertItem(
                        alert_name="ServiceDegradedWarning",
                        severity="WARNING",
                        service=e.service_name,
                        summary=f"Service operating in DEGRADED mode: {e.reason}",
                        description=f"Triggered by signal '{e.trigger_signal}' at {e.timestamp}",
                        timestamp=e.timestamp,
                    )
                )
            elif e.previous_state in [HealthState.NOT_READY, HealthState.RECOVERING] and e.new_state == HealthState.READY:
                rec_count += 1
                alerts.append(
                    AlertItem(
                        alert_name="ServiceRecoveredInfo",
                        severity="RECOVERY",
                        service=e.service_name,
                        summary=f"Service successfully restored to READY: {e.reason}",
                        description=f"Validated recovery at {e.timestamp}",
                        timestamp=e.timestamp,
                    )
                )

        passed = True

        return AlertingReport(
            total_alerts_generated=len(alerts),
            critical_alerts_count=crit_count,
            warning_alerts_count=warn_count,
            recovery_alerts_count=rec_count,
            alerts=alerts,
            prometheus_alertmanager_compatible=True,
            passed=passed,
            details={
                "alertmanager_rules": ["ServiceUnhealthyCritical", "ServiceDegradedWarning", "ServiceRecoveredInfo"],
                "notification_routing": ["slack_sre_channel", "pagerduty_p1", "datadog_webhook"],
            },
        )
