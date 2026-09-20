"""Tests for Safety Incident Lifecycle State Machine and Event Publisher."""

import pytest
from app.safety.incidents.manager import SafetyIncidentManager
from app.safety.incidents.lifecycle import IncidentLifecycleState
from app.safety.gateway.decision import SafetyCategory, ViolationSeverity
from app.safety.events.publisher import SafetyEventPublisher, PromptInjectionDetectedEvent


def test_safety_incident_creation_and_lifecycle():
    mgr = SafetyIncidentManager()
    incident = mgr.create_incident(
        tenant_id="tenant_bank",
        title="Prompt Injection in Loan Evaluator",
        description="User attempted to override loan limit validation",
        category=SafetyCategory.PROMPT_INJECTION,
        severity=ViolationSeverity.HIGH,
        actor="safety_gateway",
    )

    assert incident.state == IncidentLifecycleState.DETECTED
    assert len(incident.audit_trail) == 1

    # Transition: DETECTED -> CLASSIFIED
    inc_classified = mgr.transition_state(
        incident_id=incident.incident_id,
        new_state=IncidentLifecycleState.CLASSIFIED,
        actor="secops_analyst",
        notes="Classified as direct injection probe",
        tenant_id="tenant_bank",
    )
    assert inc_classified.state == IncidentLifecycleState.CLASSIFIED

    # Transition: CLASSIFIED -> INVESTIGATING
    inc_investigating = mgr.transition_state(
        incident_id=incident.incident_id,
        new_state=IncidentLifecycleState.INVESTIGATING,
        actor="secops_analyst",
        tenant_id="tenant_bank",
    )
    assert inc_investigating.state == IncidentLifecycleState.INVESTIGATING

    # Transition: INVESTIGATING -> MITIGATED
    inc_mitigated = mgr.transition_state(
        incident_id=incident.incident_id,
        new_state=IncidentLifecycleState.MITIGATED,
        actor="secops_analyst",
        notes="Blocked originating IP and added rule",
        tenant_id="tenant_bank",
    )
    assert inc_mitigated.state == IncidentLifecycleState.MITIGATED

    # Transition: MITIGATED -> RESOLVED
    inc_resolved = mgr.transition_state(
        incident_id=incident.incident_id,
        new_state=IncidentLifecycleState.RESOLVED,
        actor="secops_lead",
        tenant_id="tenant_bank",
    )
    assert inc_resolved.state == IncidentLifecycleState.RESOLVED
    assert inc_resolved.resolved_at is not None

    # Invalid transition should raise ValueError
    with pytest.raises(ValueError):
        mgr.transition_state(
            incident_id=incident.incident_id,
            new_state=IncidentLifecycleState.DETECTED,
            actor="secops_lead",
        )


def test_safety_event_publisher():
    publisher = SafetyEventPublisher()
    received_events = []

    def subscriber(evt):
        received_events.append(evt)

    publisher.subscribe(subscriber)
    publisher.publish(
        PromptInjectionDetectedEvent(
            tenant_id="tenant_sec",
            payload={"source": "api_chat", "attempt_count": 1},
        )
    )

    assert len(received_events) == 1
    assert received_events[0].tenant_id == "tenant_sec"
    assert len(publisher.get_events(tenant_id="tenant_sec")) == 1
