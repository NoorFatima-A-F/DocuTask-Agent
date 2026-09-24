"""Tests for SRE Automation Framework and Closed-Loop Self-Healing."""

from app.observability.alerts.engine import ActiveAlert, AlertSeverity
from app.observability.automation.actions import AutoActionType, SREActionExecutor
from app.observability.automation.framework import SREAutomationFramework


def test_sre_action_executor():
    res_restart = SREActionExecutor.restart_service("worker-service", "node-101")
    assert res_restart.success is True
    assert res_restart.action_type == AutoActionType.RESTART_SERVICE

    res_scale = SREActionExecutor.scale_workers("cluster-primary", target_worker_count=12)
    assert res_scale.success is True
    assert res_scale.action_type == AutoActionType.SCALE_WORKERS

    res_queue = SREActionExecutor.clear_stuck_queue("ingestion-queue")
    assert res_queue.success is True
    assert res_queue.action_type == AutoActionType.CLEAR_QUEUE


def test_sre_automation_closed_loop_trigger():
    framework = SREAutomationFramework()

    # Trigger alert matching high queue backlog
    alert = ActiveAlert(
        alert_id="alt-queue-99",
        rule_id="alert-queue.depth-high",
        name="Queue Backlog Exceeded Threshold",
        severity=AlertSeverity.CRITICAL,
        labels={"cluster_id": "cluster-east"},
    )

    action_res = framework.handle_alert(alert)
    assert action_res is not None
    assert action_res.action_type == AutoActionType.SCALE_WORKERS
    assert action_res.target == "cluster-east"

    # Cooldown should prevent immediate duplicate execution
    action_res2 = framework.handle_alert(alert)
    assert action_res2 is None
