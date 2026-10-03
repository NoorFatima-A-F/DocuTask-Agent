"""
Tests for Incident Management, State Machine Transitions, and Alerting Notifications.
"""

import pytest

from app.infrastructure.incidents.models import (
    Incident,
    IncidentStatus,
)
from app.infrastructure.incidents.lifecycle import (
    IncidentLifecycleStateMachine,
    InvalidIncidentTransitionError,
)
from app.infrastructure.incidents.notifications import (
    IncidentNotifier,
    NotificationChannel,
    NotificationMessage,
)
from app.infrastructure.incidents.manager import (
    IncidentManager,
)
from app.infrastructure.reliability.models import SeverityLevel


def test_incident_lifecycle_transitions():
    incident = Incident(
        incident_id="inc-test-01",
        title="Elevated Error Rate on OCR",
        severity=SeverityLevel.MAJOR,
        impacted_components=["ocr-service"],
    )

    assert incident.status == IncidentStatus.DETECTED

    # DETECTED -> INVESTIGATING
    IncidentLifecycleStateMachine.transition(incident, IncidentStatus.INVESTIGATING, actor="oncall", message="Assigned oncall engineer")
    assert incident.status == IncidentStatus.INVESTIGATING

    # INVESTIGATING -> IDENTIFIED
    IncidentLifecycleStateMachine.transition(incident, IncidentStatus.IDENTIFIED, actor="oncall", message="Identified memory leak in worker pool")
    assert incident.status == IncidentStatus.IDENTIFIED

    # IDENTIFIED -> MITIGATING
    IncidentLifecycleStateMachine.transition(incident, IncidentStatus.MITIGATING, actor="oncall", message="Restarting worker pool")
    assert incident.status == IncidentStatus.MITIGATING

    # MITIGATING -> RESOLVED
    IncidentLifecycleStateMachine.transition(incident, IncidentStatus.RESOLVED, actor="oncall", message="Error rate dropped below threshold")
    assert incident.status == IncidentStatus.RESOLVED
    assert incident.resolved_at is not None

    # RESOLVED -> POSTMORTEM
    IncidentLifecycleStateMachine.transition(incident, IncidentStatus.POSTMORTEM, actor="sre", message="PIR doc scheduled")
    assert incident.status == IncidentStatus.POSTMORTEM

    # POSTMORTEM -> CLOSED
    IncidentLifecycleStateMachine.transition(incident, IncidentStatus.CLOSED, actor="sre", message="PIR completed")
    assert incident.status == IncidentStatus.CLOSED
    assert incident.closed_at is not None
    assert len(incident.timeline) == 6


def test_invalid_incident_transition():
    incident = Incident(
        incident_id="inc-test-02",
        title="Database Latency",
        severity=SeverityLevel.CRITICAL,
    )

    # Cannot transition directly from DETECTED to POSTMORTEM
    with pytest.raises(InvalidIncidentTransitionError):
        IncidentLifecycleStateMachine.transition(incident, IncidentStatus.POSTMORTEM)


def test_incident_notifier_dispatch_and_rate_limiting():
    notifier = IncidentNotifier(rate_limit_cooldown_seconds=1.0)
    received = []

    def mock_slack_handler(msg: NotificationMessage) -> bool:
        received.append(msg)
        return True

    notifier.register_channel_handler(NotificationChannel.SLACK, mock_slack_handler)

    msg1 = notifier.dispatch(
        message_id="msg-1",
        incident_id="inc-100",
        channel=NotificationChannel.SLACK,
        severity=SeverityLevel.WARNING,
        title="High CPU Alert",
        content="CPU usage > 85%",
    )
    assert msg1 is not None
    assert len(received) == 1

    # Second immediate dispatch for same incident & channel should be suppressed by rate limit
    msg2 = notifier.dispatch(
        message_id="msg-2",
        incident_id="inc-100",
        channel=NotificationChannel.SLACK,
        severity=SeverityLevel.WARNING,
        title="High CPU Alert again",
        content="CPU usage > 85%",
    )
    assert msg2 is None
    assert len(received) == 1


def test_incident_manager_end_to_end():
    manager = IncidentManager()

    # Create critical incident (triggers PAGERDUTY and EVENT_BUS alerts)
    inc = manager.create_incident(
        incident_id="inc-e2e-01",
        title="Total Cluster Partition",
        severity=SeverityLevel.CRITICAL,
        impacted_components=["cluster-us-east-1"],
        lead_responder="alice@docutask.internal",
    )

    assert inc.incident_id == "inc-e2e-01"
    assert len(manager.list_active_incidents()) == 1

    # Escalate severity
    manager.escalate_severity("inc-e2e-01", SeverityLevel.CATASTROPHIC, reason="Multiple regions affected")
    assert inc.severity == SeverityLevel.CATASTROPHIC

    # Resolve incident
    manager.transition_incident("inc-e2e-01", IncidentStatus.RESOLVED, message="Traffic restored")
    assert inc.status == IncidentStatus.RESOLVED
    assert len(manager.list_active_incidents()) == 0
