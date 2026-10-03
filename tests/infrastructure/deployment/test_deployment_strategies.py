"""Tests for Rolling, Canary, Blue/Green, and Shadow Deployment Strategies."""

from app.infrastructure.deployment.strategies import (
    RollingStrategyConfig,
    RollingDeploymentStrategy,
    CanaryDeploymentStrategy,
    BlueGreenDeploymentStrategy,
    ShadowDeploymentStrategy,
)


def test_rolling_deployment_strategy() -> None:
    rolling = RollingDeploymentStrategy(RollingStrategyConfig(batch_size=2))
    upgraded_batches = []

    def upgrade_fn(start: int, count: int) -> bool:
        upgraded_batches.append((start, count))
        return True

    ok = rolling.execute(total_instances=5, upgrade_batch_fn=upgrade_fn)
    assert ok is True
    assert upgraded_batches == [(0, 2), (2, 2), (4, 1)]


def test_canary_deployment_strategy_success_and_failure() -> None:
    canary = CanaryDeploymentStrategy(max_error_rate=0.02)
    weights_applied = []

    # Successful rollout
    ok = canary.execute(
        set_weight_fn=lambda w: weights_applied.append(w),
        evaluate_metrics_fn=lambda w: {"error_rate": 0.005},
    )
    assert ok is True
    assert weights_applied == [1.0, 5.0, 25.0, 50.0, 100.0]

    # Rollout halting on error spike at 25%
    weights_failing = []
    failed_ok = canary.execute(
        set_weight_fn=lambda w: weights_failing.append(w),
        evaluate_metrics_fn=lambda w: {"error_rate": 0.05 if w >= 25.0 else 0.001},
    )
    assert failed_ok is False
    assert weights_failing == [1.0, 5.0, 25.0]


def test_blue_green_and_shadow_strategies() -> None:
    # Blue/Green
    bg = BlueGreenDeploymentStrategy()
    events = []
    bg_ok = bg.execute(
        deploy_green_fn=lambda: events.append("deploy_green") or True,
        verify_green_fn=lambda: events.append("verify_green") or True,
        switch_traffic_to_green_fn=lambda: events.append("switch_traffic") or True,
        shutdown_blue_fn=lambda: events.append("shutdown_blue"),
    )
    assert bg_ok is True
    assert events == ["deploy_green", "verify_green", "switch_traffic", "shutdown_blue"]

    # Shadow
    shadow = ShadowDeploymentStrategy()
    shadow_res = shadow.execute(
        enable_shadow_fn=lambda: True,
        collect_comparison_metrics_fn=lambda: {"drift_rate": 0.01, "latency_diff_ms": -2.1},
        disable_shadow_fn=lambda: True,
    )
    assert shadow_res["status"] == "completed"
    assert shadow_res["shadow_metrics"]["drift_rate"] == 0.01
