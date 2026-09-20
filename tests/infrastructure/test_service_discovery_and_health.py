"""Tests for Service Registry, Dependency Validation, Discovery, and Health Monitoring."""

from app.infrastructure.services.discovery import ServiceDiscovery
from app.infrastructure.services.health import (
    HealthStatus,
    ServiceHealthMonitor,
)
from app.infrastructure.services.registry import ServiceRegistry


def test_service_registration_and_dependencies():
    reg = ServiceRegistry()

    # Register workflow-engine first
    wf = reg.register_service(name="workflow-engine", version="1.0.0")
    assert wf.service_id == "svc_workflow-engine_production"

    # Register agent-runtime depending on workflow-engine
    agent_svc = reg.register_service(
        name="agent-runtime",
        version="1.0.0",
        dependencies=["workflow-engine"],
    )

    valid, missing = reg.validate_dependencies(agent_svc.service_id)
    assert valid is True
    assert len(missing) == 0

    # Register service with missing dependency
    orphan = reg.register_service(name="orphan-service", dependencies=["non-existent-service"])
    valid_o, missing_o = reg.validate_dependencies(orphan.service_id)
    assert valid_o is False
    assert len(missing_o) == 1


def test_service_discovery_resolution():
    reg = ServiceRegistry()
    discovery = ServiceDiscovery(reg)

    # Custom endpoint
    discovery.register_endpoint("agent-runtime", "PRODUCTION", "http://agent-mesh.internal:8080")
    resolved = discovery.resolve_endpoint("agent-runtime", "PRODUCTION")
    assert resolved == "http://agent-mesh.internal:8080"

    # Fallback endpoint
    fallback = discovery.resolve_endpoint("workflow-engine", "PRODUCTION")
    assert "workflow-engine.production.svc.cluster.local" in fallback


def test_service_health_monitor():
    monitor = ServiceHealthMonitor()

    # Record healthy
    h1 = monitor.record_health(
        service_id="svc_doc_worker",
        status=HealthStatus.HEALTHY,
        cpu_percent=25.0,
        latency_p95_ms=15.0,
    )
    assert h1.status == HealthStatus.HEALTHY

    # Record unhealthy
    monitor.record_health(
        service_id="svc_database",
        status=HealthStatus.UNHEALTHY,
        cpu_percent=98.0,
        errors_per_minute=120,
    )

    unhealthy_list = monitor.list_unhealthy_services()
    assert len(unhealthy_list) == 1
    assert unhealthy_list[0].service_id == "svc_database"
