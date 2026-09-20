"""Tests for Dynamic Service Discovery, Registry, Resolver, and Heartbeat."""

import pytest
from app.infrastructure.networking.discovery import (
    ServiceDiscoveryRegistry,
    ServiceRegistration,
    ServiceHealthState,
    ServiceResolver,
    ServiceHeartbeatManager,
)


def test_service_registration_and_query() -> None:
    registry = ServiceDiscoveryRegistry()
    reg = ServiceRegistration(
        service_name="document-ocr-worker",
        host="10.0.1.15",
        port=8443,
        namespace="workers",
        region="us-east-1",
        capabilities=["ocr", "tesseract"],
        labels={"tier": "gpu"},
    )
    inst = registry.register_instance(reg)

    assert inst.instance_id is not None
    assert inst.service_name == "document-ocr-worker"
    assert inst.health_state == ServiceHealthState.HEALTHY
    assert inst.address == "10.0.1.15:8443"

    # Query with capability
    found = registry.get_instances_for_service("document-ocr-worker", capability="ocr")
    assert len(found) == 1
    assert found[0].instance_id == inst.instance_id

    # Query with non-matching capability
    not_found = registry.get_instances_for_service("document-ocr-worker", capability="speech-to-text")
    assert len(not_found) == 0


def test_service_resolver_with_aliases_and_multi_region_failover() -> None:
    registry = ServiceDiscoveryRegistry()
    resolver = ServiceResolver(registry)

    # Register in us-west-2
    reg_west = ServiceRegistration(
        service_name="agent-executor",
        host="10.2.0.50",
        port=9090,
        region="us-west-2",
    )
    registry.register_instance(reg_west)

    # Register alias
    resolver.register_alias("ai-agent", "agent-executor")

    # Local region (us-east-1) has no instances -> should failover to us-west-2
    resolved = resolver.resolve("ai-agent", caller_region="us-east-1")
    assert resolved is not None
    assert resolved.service_name == "agent-executor"
    assert resolved.region == "us-west-2"
    assert resolved.resolved_via == "multi-region-failover"


def test_service_heartbeat_and_stale_eviction() -> None:
    registry = ServiceDiscoveryRegistry()
    heartbeat_mgr = ServiceHeartbeatManager(registry)

    reg = ServiceRegistration(
        service_name="transient-worker",
        host="10.0.9.9",
        port=8080,
        ttl_seconds=1,
    )
    inst = registry.register_instance(reg)

    # Update heartbeat
    assert heartbeat_mgr.record_heartbeat(inst.instance_id, active_connections=5, latency_ms=3.2)
    updated_inst = registry.get_instance(inst.instance_id)
    assert updated_inst.active_connections == 5

    # Simulate stale eviction with 0 grace period after manual timestamp backdating
    from datetime import datetime, timezone, timedelta
    updated_inst.last_heartbeat_at = datetime.now(timezone.utc) - timedelta(seconds=10)

    evicted = heartbeat_mgr.evict_stale_instances(grace_period_seconds=0)
    assert inst.instance_id in evicted
    assert registry.get_instance(inst.instance_id) is None
