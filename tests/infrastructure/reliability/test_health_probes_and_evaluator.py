"""
Tests for Health Probes, Heartbeat Aggregation, Flap Detection, and Health Scoring.
"""

import time
import pytest
from app.infrastructure.health.probes import (
    HealthProbe,
    ProbeRegistry,
    ProbeResult,
    ProbeStatus,
    ProbeType,
)
from app.infrastructure.health.heartbeat import (
    HeartbeatAggregator,
    HeartbeatSignal,
)
from app.infrastructure.health.evaluator import (
    FlapDetector,
    HealthEvaluator,
)
from app.infrastructure.health.aggregator import (
    HealthAggregatorService,
)


def test_probe_registry_and_sync_execution():
    registry = ProbeRegistry()

    probe = HealthProbe(
        probe_id="probe-db-liveness",
        component_id="primary-db",
        probe_type=ProbeType.LIVENESS,
        consecutive_failure_threshold=2,
    )

    is_db_up = [True]

    def db_check():
        return is_db_up[0]

    registry.register_probe(probe, handler=db_check)

    # 1. Successful check
    res1 = registry.execute_probe_sync("probe-db-liveness")
    assert res1.status == ProbeStatus.HEALTHY
    assert registry.get_probe_status("probe-db-liveness") == ProbeStatus.HEALTHY

    # 2. First failure (still requires 2 consecutive to transition status)
    is_db_up[0] = False
    res2 = registry.execute_probe_sync("probe-db-liveness")
    assert res2.status == ProbeStatus.UNHEALTHY
    assert registry.get_probe_status("probe-db-liveness") == ProbeStatus.HEALTHY

    # 3. Second consecutive failure triggers status change to UNHEALTHY
    res3 = registry.execute_probe_sync("probe-db-liveness")
    assert registry.get_probe_status("probe-db-liveness") == ProbeStatus.UNHEALTHY


@pytest.mark.anyio
async def test_probe_registry_async_execution():
    registry = ProbeRegistry()

    probe = HealthProbe(
        probe_id="probe-ai-readiness",
        component_id="ai-gateway",
        probe_type=ProbeType.READINESS,
        timeout_seconds=0.5,
    )

    async def ai_check():
        return {"status": "HEALTHY", "metrics": {"tps": 120}}

    registry.register_probe(probe, async_handler=ai_check)

    res = await registry.execute_probe_async("probe-ai-readiness")
    assert res.status == ProbeStatus.HEALTHY
    assert res.metrics.get("tps") == 120


def test_heartbeat_aggregator():
    aggregator = HeartbeatAggregator(default_stale_threshold_seconds=0.1)

    signal = HeartbeatSignal(
        entity_id="node-worker-01",
        entity_type="worker_node",
        ttl_seconds=0.2,
        cpu_usage_percent=42.5,
    )

    st = aggregator.record_heartbeat(signal)
    assert st.is_alive
    assert not st.is_stale
    assert st.entity_id == "node-worker-01"

    # Wait for TTL to expire
    time.sleep(0.25)
    st_dead = aggregator.get_status("node-worker-01")
    assert not st_dead.is_alive
    assert st_dead.is_stale
    assert len(aggregator.get_dead_entities()) == 1


def test_flap_detection():
    detector = FlapDetector(window_seconds=1.0, flap_threshold_transitions=4)

    assert not detector.record_status("comp-1", ProbeStatus.HEALTHY)
    assert not detector.record_status("comp-1", ProbeStatus.UNHEALTHY)
    assert not detector.record_status("comp-1", ProbeStatus.HEALTHY)
    # 4th transition within window triggers flapping
    assert detector.record_status("comp-1", ProbeStatus.UNHEALTHY)
    assert detector.is_flapping("comp-1")


def test_health_evaluator_and_aggregator_service():
    registry = ProbeRegistry()
    evaluator = HealthEvaluator(probe_registry=registry)
    service = HealthAggregatorService(probe_registry=registry, health_evaluator=evaluator)

    # Register multiple probes for a component
    p1 = HealthProbe(probe_id="p1", component_id="ocr-service", probe_type=ProbeType.LIVENESS)
    p2 = HealthProbe(probe_id="p2", component_id="ocr-service", probe_type=ProbeType.READINESS)
    registry.register_probe(p1, handler=lambda: True)
    registry.register_probe(p2, handler=lambda: True)

    registry.execute_probe_sync("p1")
    registry.execute_probe_sync("p2")

    score = service.get_component_health("ocr-service")
    assert score.overall_status == ProbeStatus.HEALTHY
    assert score.score == 100.0

    matrix = service.get_system_health_matrix()
    assert matrix.total_components == 1
    assert matrix.healthy_count == 1
    assert matrix.unhealthy_count == 0
