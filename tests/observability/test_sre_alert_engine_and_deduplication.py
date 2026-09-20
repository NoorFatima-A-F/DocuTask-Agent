"""Tests for Alert Rules, Alert Engine Lifecycle, and Router Dispatch."""

import pytest
from app.observability.alerts.engine import ActiveAlert, AlertEngine, AlertState
from app.observability.alerts.notifications import AlertRouter, ChannelType, NotificationChannel
from app.observability.alerts.rules import AlertRule, AlertSeverity, RuleConditionType
from app.observability.metrics.registry import MetricRegistry


def test_alert_engine_fire_and_resolve():
    registry = MetricRegistry()
    cpu_gauge = registry.gauge("node_cpu_usage_percent")
    cpu_gauge.set(95.0)

    engine = AlertEngine(metric_registry=registry)
    rule = AlertRule(
        rule_id="alert-cpu-high",
        name="High CPU Usage",
        severity=AlertSeverity.CRITICAL,
        metric_name="node_cpu_usage_percent",
        operator=">",
        threshold_value=90.0,
        description="Node CPU exceeded 90%",
    )
    engine.add_rule(rule)

    # 1. Evaluate when CPU > 90% -> should fire
    fired = engine.evaluate_metrics()
    assert len(fired) == 1
    assert fired[0].name == "High CPU Usage"
    assert len(engine.list_active_alerts()) == 1

    # 2. Acknowledge alert
    ack_ok = engine.acknowledge_alert(fired[0].alert_id, "sre_lead")
    assert ack_ok is True

    # 3. CPU drops back to 50% -> should resolve
    cpu_gauge.set(50.0)
    engine.evaluate_metrics()
    assert len(engine.list_active_alerts()) == 0
    assert len(engine.get_alert_history()) == 1


def test_alert_router_dispatch():
    router = AlertRouter()
    channel = NotificationChannel(
        channel_id="slack-sre",
        name="Slack SRE OnCall",
        channel_type=ChannelType.SLACK,
        endpoint="https://hooks.slack.com/services/xxx",
        min_severity=AlertSeverity.WARNING,
    )
    router.register_channel(channel)

    alert = ActiveAlert(
        alert_id="alt-1",
        rule_id="rule-1",
        name="Disk Full",
        severity=AlertSeverity.CRITICAL,
    )
    dispatched = router.dispatch(alert)
    assert len(dispatched) == 1
    assert dispatched[0].channel_id == "slack-sre"
    assert dispatched[0].success is True
