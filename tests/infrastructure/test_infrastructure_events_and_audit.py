"""Tests for Infrastructure Event System and Compliance Auditing."""

from app.infrastructure.events.publisher import InfrastructureEventPublisher
from app.infrastructure.events.schemas import InfrastructureEventType


def test_event_publisher_and_subscription():
    publisher = InfrastructureEventPublisher()
    events_received = []

    publisher.subscribe(
        InfrastructureEventType.SERVICE_STARTED,
        lambda evt: events_received.append(evt),
    )

    # Publish matching event
    evt = publisher.publish(
        event_type=InfrastructureEventType.SERVICE_STARTED,
        service_name="agent-worker",
        environment="PRODUCTION",
        payload={"worker_id": "w1"},
    )
    assert evt.event_type == InfrastructureEventType.SERVICE_STARTED
    assert len(events_received) == 1
    assert events_received[0].service_name == "agent-worker"


def test_audit_event_recording():
    publisher = InfrastructureEventPublisher()

    audit = publisher.record_audit(
        actor="lead_devops",
        action="drain_node",
        resource="node_04",
        environment="PRODUCTION",
        result="SUCCESS",
        metadata={"reason": "Kernel security patch"},
    )

    assert audit.audit_id.startswith("infaud_")
    assert audit.actor == "lead_devops"
    assert audit.result == "SUCCESS"

    audits = publisher.get_audits(environment="PRODUCTION")
    assert len(audits) >= 1
