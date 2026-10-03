"""Tests for Prompt Telemetry Analytics, Alerting, and A/B Testing (Phase 8D)."""

from app.prompts.monitoring.metrics import PromptExecutionEvent
from app.prompts.monitoring.analytics import PromptAnalyticsEngine
from app.prompts.monitoring.alerts import PromptAlertManager
from app.prompts.optimization.experiments import PromptVariant
from app.prompts.optimization.ab_testing import PromptABTestingService


def test_prompt_telemetry_analytics_and_alerting():
    analytics = PromptAnalyticsEngine()
    alert_mgr = PromptAlertManager(max_error_rate=0.05, max_latency_ms=2000.0)

    for i in range(10):
        event = PromptExecutionEvent(
            event_id=f"evt_{i}",
            prompt_id="prompt_a",
            version_id="v_1_0_0",
            organization_id="org_test",
            model_id="gpt-4o",
            prompt_tokens=100,
            completion_tokens=50,
            latency_ms=150.0 + i * 10,
            cost_usd=0.001,
            is_success=True if i < 9 else False,
        )
        analytics.record_event(event)

    summary = analytics.get_prompt_summary("prompt_a", "org_test")
    assert summary.total_invocations == 10
    assert summary.successful_invocations == 9
    assert summary.failed_invocations == 1
    assert summary.success_rate_pct == 90.0

    # Test alert trigger on 10% error rate (threshold 5%)
    alerts = alert_mgr.check_health("prompt_a", "org_test", error_rate=0.10, avg_latency_ms= summary.avg_latency_ms)
    assert len(alerts) >= 1
    assert alerts[0].alert_type == "ERROR_SPIKE"


def test_ab_testing_experiment_flow():
    ab_service = PromptABTestingService()

    v_a = PromptVariant(variant_id="var_a", version_id="v_1_0", traffic_weight=0.5)
    v_b = PromptVariant(variant_id="var_b", version_id="v_2_0", traffic_weight=0.5)

    exp = ab_service.create_experiment(
        experiment_id="exp_summary_v1_v2",
        prompt_id="summary_prompt",
        name="Summary v1 vs v2",
        organization_id="org_test",
        variants=[v_a, v_b],
    )

    # Record 20 outcomes: var_a has 70% success, var_b has 100% success with positive feedback
    for _ in range(7):
        ab_service.record_outcome("exp_summary_v1_v2", "var_a", is_success=True)
    for _ in range(3):
        ab_service.record_outcome("exp_summary_v1_v2", "var_a", is_success=False)

    for _ in range(10):
        ab_service.record_outcome("exp_summary_v1_v2", "var_b", is_success=True, positive_feedback=True)

    winner = ab_service.conclude_experiment("exp_summary_v1_v2")
    assert winner is not None
    assert winner.variant_id == "var_b"
    assert exp.status.value == "CONCLUDED"
