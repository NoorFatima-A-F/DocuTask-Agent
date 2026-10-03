"""Tests for Audit Collection Gateway, Normalization, and Enrichment Processors."""

from app.audit.collector.gateway import AuditCollectorGateway
from app.audit.collector.normalizer import EventNormalizer
from app.audit.core.events import EventCategory, ActorType, AuditSeverity, OutcomeType


def test_event_normalizer_dict_and_enum_conversion():
    normalizer = EventNormalizer()
    raw = {
        "event_type": "model.invoke",
        "category": "ai",
        "tenant_id": "tenant_norm",
        "actor_id": "user_42",
        "actor_type": "user",
        "action": "generate",
        "resource_type": "model",
        "resource_id": "gemini-1.5-flash",
        "severity": "info",
        "outcome": "success",
    }
    event = normalizer.normalize(raw)
    assert event.category == EventCategory.AI
    assert event.actor_type == ActorType.USER
    assert event.severity == AuditSeverity.INFO
    assert event.outcome == OutcomeType.SUCCESS
    assert event.event_id.startswith("aud_evt_")


def test_collector_gateway_enrichment_and_recording():
    gateway = AuditCollectorGateway()
    
    # Ingest using kwargs
    event = gateway.record(
        event_type="workflow.start",
        tenant_id="tenant_gate",
        actor_id="admin_1",
        action="start",
        resource_type="workflow",
        resource_id="wf_001",
        metadata={"custom_tag": "test_tag"},
    )

    assert event.integrity_hash is not None
    assert event.metadata["collector_version"] == "8G.1.0"
    assert event.metadata["custom_tag"] == "test_tag"

    # Verify event stored in repository
    fetched = gateway.repository.get_by_id(event.event_id, tenant_id="tenant_gate")
    assert fetched is not None
    assert fetched.action == "start"


def test_collector_gateway_batch_recording():
    gateway = AuditCollectorGateway()
    batch = [
        {"event_type": f"step_{i}", "tenant_id": "tenant_batch", "actor_id": "u", "action": "run", "resource_type": "step", "resource_id": f"s_{i}"}
        for i in range(5)
    ]
    recorded = gateway.record_batch(batch)
    assert len(recorded) == 5
    assert len(gateway.repository.list_by_tenant("tenant_batch")) == 5
