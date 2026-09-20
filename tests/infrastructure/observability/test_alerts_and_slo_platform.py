"""
Tests for Alert Rule Evaluation, Routing, Throttling, and SLO Error Budgets.
"""

import pytest

from app.infrastructure.observability.alerts.models import (
    AlertInstance,
    AlertRule,
    AlertSeverity,
    AlertStatus,
    RuleType,
)
from app.infrastructure.observability.alerts.rules import (
    AlertRuleEvaluator,
)
from app.infrastructure.observability.alerts.routing import (
    AlertRouteRule,
    AlertRouter,
)
from app.infrastructure.observability.alerts.notifications import (
    AlertDispatcher,
)
from app.infrastructure.observability.slo.objectives import (
    SLIIndicator,
    SLIType,
    SLOObjective,
)
from app.infrastructure.observability.slo.budgets import (
    ErrorBudgetStatus,
    ErrorBudgetTracker,
)


def test_alert_rule_evaluation_and_auto_resolve():
    evaluator = AlertRuleEvaluator()
    rule = AlertRule(
        rule_id="rule-cpu-high",
        name="High CPU Utilization",
        metric_name="system_cpu_usage_percent",
        comparator=">",
        threshold_value=80.0,
        severity=AlertSeverity.CRITICAL,
        team="infra",
    )
    evaluator.register_rule(rule)

    # 1. Normal metric -> no alert
    res_normal = evaluator.evaluate("rule-cpu-high", current_value=65.0)
    assert res_normal is None
    assert len(evaluator.list_active_alerts()) == 0

    # 2. Breached metric -> Alert FIRES
    res_breach = evaluator.evaluate("rule-cpu-high", current_value=88.5, service_name="worker-01")
    assert res_breach is not None
    assert res_breach.status == AlertStatus.FIRING
    assert res_breach.severity == AlertSeverity.CRITICAL
    assert len(evaluator.list_active_alerts()) == 1

    # 3. Metric recovers -> Alert RESOLVES
    res_recovered = evaluator.evaluate("rule-cpu-high", current_value=50.0, service_name="worker-01")
    assert res_recovered is not None
    assert res_recovered.status == AlertStatus.RESOLVED
    assert len(evaluator.list_active_alerts()) == 0


def test_alert_routing_and_dispatcher():
    router = AlertRouter()
    router.add_route(AlertRouteRule(
        route_id="route-sre-critical",
        team="sre",
        min_severity=AlertSeverity.CRITICAL,
        channels=["pagerduty-sre", "slack-incidents"],
    ))

    dispatcher = AlertDispatcher(router=router, cooldown_seconds=0.1)

    sent_channels = []

    def mock_channel_handler(alert: AlertInstance, ch: str) -> bool:
        sent_channels.append(ch)
        return True

    dispatcher.register_channel_handler("pagerduty-sre", mock_channel_handler)
    dispatcher.register_channel_handler("slack-incidents", mock_channel_handler)

    alert = AlertInstance(
        rule_id="r1",
        rule_name="Database Connection Exhaustion",
        severity=AlertSeverity.CRITICAL,
        team="sre",
        current_value=100.0,
        threshold_value=90.0,
        message="Connections maxed",
        fingerprint="fp-db-1",
    )

    dispatched = dispatcher.dispatch(alert)
    assert len(dispatched) == 2
    assert "pagerduty-sre" in sent_channels
    assert "slack-incidents" in sent_channels


def test_slo_and_error_budget_tracking():
    tracker = ErrorBudgetTracker()

    # 99.9% Availability SLO
    slo = SLOObjective(
        slo_id="slo-api-availability",
        name="API Gateway Availability",
        service_name="api-gateway",
        sli_type=SLIType.AVAILABILITY,
        target_percent=99.9,
    )
    tracker.register_slo(slo)

    # 10,000 total events: 9,995 good, 5 bad
    # Allowed bad for 99.9% is 10,000 * 0.001 = 10 bad events
    tracker.record_events("slo-api-availability", good_count=9995, bad_count=5)

    status = tracker.evaluate_budget("slo-api-availability")
    assert status.total_events == 10000
    assert status.bad_events == 5
    assert status.allowed_bad_events == 10.0
    assert status.current_compliance_percent == 99.95
    assert status.remaining_budget_percent == 50.0  # 5 of 10 used -> 50% left
    assert not status.is_exhausted
