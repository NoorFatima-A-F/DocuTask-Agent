"""Unit tests for Progressive Delivery Strategies Engine."""
import pytest
from app.deployment.core.exceptions import StrategyExecutionException
from app.deployment.strategies.blue_green import BlueGreenPhase, BlueGreenStrategy
from app.deployment.strategies.canary import CanaryStrategy
from app.deployment.strategies.rolling import RollingStrategy
from app.deployment.strategies.shadow import ShadowStrategy


def test_rolling_strategy_success():
    rolling = RollingStrategy(batch_size=2)
    results = rolling.execute(total_replicas=6)

    assert len(results) == 3
    assert results[-1].updated_replicas == 6
    assert all(r.healthy for r in results)


def test_rolling_strategy_health_failure():
    def failing_health():
        return False

    rolling = RollingStrategy(batch_size=1, health_check_fn=failing_health)
    with pytest.raises(StrategyExecutionException, match="failed health verification"):
        rolling.execute(total_replicas=3)


def test_blue_green_full_lifecycle():
    bg = BlueGreenStrategy()
    assert bg.live_slot.name == "blue"
    assert bg.idle_slot.name == "green"

    bg.provision_standby("rel-2.0.0")
    assert bg.phase == BlueGreenPhase.GREEN_PROVISIONED

    bg.verify_standby()
    assert bg.phase == BlueGreenPhase.GREEN_VERIFIED

    bg.cutover()
    assert bg.live_slot.name == "green"
    assert bg.idle_slot.name == "blue"
    assert bg.phase == BlueGreenPhase.TRAFFIC_SWITCHED

    # Rollback
    bg.rollback()
    assert bg.live_slot.name == "blue"
    assert bg.phase == BlueGreenPhase.ROLLED_BACK


def test_canary_strategy_progression_and_abort():
    # Scenario 1: Healthy progression
    canary = CanaryStrategy(steps=[10, 50, 100], max_error_rate=0.01)
    results = canary.execute(lambda idx, pct: (0.002, 120.0))
    assert len(results) == 3
    assert all(r.passed for r in results)

    # Scenario 2: Unhealthy step abort
    canary_failing = CanaryStrategy(steps=[10, 50, 100], max_error_rate=0.01)
    with pytest.raises(StrategyExecutionException, match="Canary rollout automatically aborted"):
        canary_failing.execute(lambda idx, pct: (0.05, 120.0))


def test_shadow_strategy_traffic_parity():
    shadow = ShadowStrategy()
    for _ in range(10):
        shadow.record_comparison(
            primary_status=200,
            shadow_status=200,
            primary_latency=50.0,
            shadow_latency=52.0,
            payload_match=True,
        )

    assert shadow.calculate_parity_score() == 1.0
    metrics = shadow.get_latency_metrics()
    assert metrics["primary_avg_ms"] == 50.0
    assert shadow.is_ready_for_promotion() is True
