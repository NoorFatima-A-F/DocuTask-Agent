"""Tests for Investigation Cases, FSM Transitions, and Case Timelines."""

import pytest
from app.audit.investigations.cases import CaseLifecycleState, InvestigationManager
from app.audit.investigations.timeline import InvestigationTimelineBuilder
from app.audit.storage.repository import AuditRepository
from app.audit.evidence.manager import EvidenceManager
from app.audit.evidence.artifacts import EvidenceType
from app.audit.core.events import AuditEvent


def test_investigation_case_lifecycle():
    mgr = InvestigationManager()
    case = mgr.create_case(
        tenant_id="tenant_inv",
        title="Unauthorized Database Dump Attempt",
        summary="Suspected insider threat attempting large bulk export",
        severity="CRITICAL",
        assigned_to="lead_secops",
    )

    assert case.state == CaseLifecycleState.OPEN

    # Transition: OPEN -> TRIAGED
    c1 = mgr.transition_state(case.case_id, CaseLifecycleState.TRIAGED, actor="lead_secops", notes="Assigned severity critical", tenant_id="tenant_inv")
    assert c1.state == CaseLifecycleState.TRIAGED

    # Transition: TRIAGED -> INVESTIGATING
    c2 = mgr.transition_state(case.case_id, CaseLifecycleState.INVESTIGATING, actor="lead_secops", tenant_id="tenant_inv")
    assert c2.state == CaseLifecycleState.INVESTIGATING

    # Transition: INVESTIGATING -> EVIDENCE_COLLECTED
    c3 = mgr.transition_state(case.case_id, CaseLifecycleState.EVIDENCE_COLLECTED, actor="lead_secops", tenant_id="tenant_inv")
    assert c3.state == CaseLifecycleState.EVIDENCE_COLLECTED

    # Transition: EVIDENCE_COLLECTED -> RESOLVED
    c4 = mgr.transition_state(case.case_id, CaseLifecycleState.RESOLVED, actor="lead_secops", tenant_id="tenant_inv")
    assert c4.state == CaseLifecycleState.RESOLVED
    assert c4.resolved_at is not None

    # Invalid transition
    with pytest.raises(ValueError, match="Invalid transition"):
        mgr.transition_state(case.case_id, CaseLifecycleState.OPEN, actor="lead_secops")


def test_investigation_timeline_builder():
    repo = AuditRepository()
    evidence_mgr = EvidenceManager(repository=repo)
    investigation_mgr = InvestigationManager()
    builder = InvestigationTimelineBuilder(repository=repo, evidence_manager=evidence_mgr)

    tenant_id = "tenant_timeline"

    ev = repo.record(
        AuditEvent(
            event_id="ev_inv_1",
            event_type="secret.access",
            tenant_id=tenant_id,
            actor_id="bad_actor",
            action="access",
            resource_type="secret",
            resource_id="api_key_prod",
        )
    )

    art = evidence_mgr.create_artifact(
        tenant_id=tenant_id,
        name="Network PCAP Dump",
        evidence_type=EvidenceType.EXECUTION_EVIDENCE,
        source="ids_sensor",
        content="pcap_binary_data",
    )

    case = investigation_mgr.create_case(
        tenant_id=tenant_id,
        title="Key Compromise Investigation",
        summary="Investigating unauthorized API key access",
        event_ids=[ev.event_id],
        evidence_ids=[art.evidence_id],
    )

    timeline = builder.build_timeline(case)
    assert timeline.total_items == 2
    types = {item.item_type for item in timeline.items}
    assert "EVENT" in types
    assert "EVIDENCE" in types
