"""Tests for Incident Management Lifecycle and Postmortem Generation."""

import pytest
from app.observability.incidents.manager import (
    IncidentManager,
    IncidentSeverity,
    IncidentStatus,
)
from app.observability.incidents.postmortem import (
    PostmortemGenerator,
    PreventativeAction,
)


def test_incident_lifecycle_state_transitions():
    mgr = IncidentManager()

    inc = mgr.create_incident(
        title="Payment Gateway Timeout Spike",
        description="Increased error rate in payment settlement pipeline",
        severity=IncidentSeverity.SEV1_CRITICAL,
        affected_services=["payment-service", "billing-worker"],
    )
    assert inc.status == IncidentStatus.DETECTED

    # Acknowledge
    assert mgr.transition_status(inc.incident_id, IncidentStatus.ACKNOWLEDGED, "SRE Commander") is True
    # Assign Commander
    assert mgr.assign_commander(inc.incident_id, "Alice SRE", "SRE Commander") is True
    assert inc.commander == "Alice SRE"

    # Mitigate
    mgr.record_mitigation_action(inc.incident_id, "Alice SRE", "Restarted payment pods and enabled rate limits")
    assert mgr.transition_status(inc.incident_id, IncidentStatus.MITIGATED, "Alice SRE") is True

    # Resolve
    assert mgr.transition_status(inc.incident_id, IncidentStatus.RESOLVED, "Alice SRE") is True
    assert inc.resolved_at is not None
    assert len(inc.timeline.list_entries()) >= 4


def test_postmortem_generation():
    mgr = IncidentManager()
    inc = mgr.create_incident(
        title="Worker OOM Crash",
        description="Workers crashed under large PDF extraction workload",
        severity=IncidentSeverity.SEV2_MAJOR,
    )
    mgr.transition_status(inc.incident_id, IncidentStatus.RESOLVED, "Alice SRE")

    pm = PostmortemGenerator.generate(
        incident=inc,
        summary="Workers exhausted RAM when processing 500MB scanned PDFs.",
        impact="32 customer jobs delayed by 14 minutes.",
        five_whys=[
            "Workers crashed due to OOM.",
            "Memory spiked during PDF page rendering.",
            "Batch size was set to 50 pages concurrently.",
            "No chunked memory buffer limit was set.",
            "Default PDF parser lacked streaming mode.",
        ],
        lessons_learned=["Enforce hard streaming memory bounds on OCR pipelines."],
        action_items=[
            PreventativeAction(
                action_id="act-1",
                description="Implement chunked streaming in PDF OCR worker",
                owner="Engineering Team",
            )
        ],
    )
    assert pm.incident_id == inc.incident_id
    assert len(pm.five_whys) == 5
    assert len(pm.action_items) == 1
    assert "Incident Chronology" in pm.timeline_markdown
