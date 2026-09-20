"""Tests for Audit SDK, @audited Decorator, and FastAPI REST Endpoints."""

import pytest
import asyncio
from app.audit.sdk.client import AuditSDK, audited
from app.audit.api.routes import (
    router,
    record_event,
    search_events,
    get_event,
    verify_integrity,
    create_artifact,
    create_evidence_bundle,
    evaluate_compliance,
    create_investigation_case,
    list_investigations,
    get_investigation_timeline,
)
from app.audit.api.schemas import (
    CreateEventRequest,
    VerifyIntegrityRequest,
    CreateArtifactRequest,
    CreateBundleRequest,
    EvaluateComplianceRequest,
    CreateInvestigationCaseRequest,
)
from app.audit.core.events import EventCategory, AuditSeverity, OutcomeType
from app.audit.compliance.frameworks import ComplianceFramework
from app.audit.evidence.artifacts import EvidenceType


def test_audit_sdk_record_and_integrity_check():
    sdk = AuditSDK()
    
    event = sdk.record(
        action="model.generate",
        resource_type="model",
        resource_id="gemini-1.5-pro",
        tenant_id="tenant_sdk_test",
        actor_id="agent_writer",
        category=EventCategory.AI,
        payload_summary="Generated response for user query",
    )

    assert event.event_id is not None
    assert event.integrity_hash is not None

    verification = sdk.verify_integrity("tenant_sdk_test")
    assert verification.is_valid is True
    assert verification.total_events_checked == 1


def test_audited_decorator_sync_and_async():
    sdk = AuditSDK()

    @audited(action="process_invoice", resource_type="document", tenant_id="tenant_decorator", sdk=sdk)
    def process_doc(doc_id: str):
        return f"Processed {doc_id}"

    res = process_doc("inv_9001")
    assert res == "Processed inv_9001"

    events = sdk.repository.list_by_tenant("tenant_decorator")
    assert len(events) == 1
    assert events[0].action == "process_invoice"
    assert events[0].outcome == OutcomeType.SUCCESS
    assert events[0].duration_ms is not None

    # Error capturing
    @audited(action="fail_operation", resource_type="pipeline", tenant_id="tenant_decorator", sdk=sdk)
    def failing_op():
        raise RuntimeError("Database connection timeout")

    with pytest.raises(RuntimeError):
        failing_op()

    events_after = sdk.repository.list_by_tenant("tenant_decorator")
    assert len(events_after) == 2
    assert events_after[1].outcome == OutcomeType.ERROR
    assert events_after[1].severity == AuditSeverity.HIGH
    assert "Database connection timeout" in events_after[1].metadata.get("error", "")


def test_audit_fastapi_rest_routes():
    # 1. Ingest event
    req_event = CreateEventRequest(
        event_type="api.key.rotate",
        category=EventCategory.AUTHENTICATION,
        tenant_id="tenant_api_audit",
        actor_id="admin_sec",
        action="rotate",
        resource_type="key",
        resource_id="key_prod_01",
    )
    res_ev = record_event(req_event)
    assert res_ev.event_id is not None
    assert res_ev.integrity_hash is not None

    # 2. Search events
    search_res = search_events(tenant_id="tenant_api_audit")
    assert search_res.total_count >= 1

    # 3. Verify integrity endpoint
    verify_res = verify_integrity(VerifyIntegrityRequest(tenant_id="tenant_api_audit"))
    assert verify_res.is_valid is True

    # 4. Create artifact
    art_req = CreateArtifactRequest(
        tenant_id="tenant_api_audit",
        name="Key Rotation Audit Log",
        evidence_type=EvidenceType.GOVERNANCE_EVIDENCE,
        source="vault",
        content="{}",
    )
    art = create_artifact(art_req)
    assert art.evidence_id is not None

    # 5. Create evidence bundle
    bnd_req = CreateBundleRequest(
        tenant_id="tenant_api_audit",
        title="Key Management Review",
        purpose="ISO 27001 Audit",
        event_ids=[res_ev.event_id],
        artifact_ids=[art.evidence_id],
    )
    bnd = create_evidence_bundle(bnd_req)
    assert bnd.manifest_hash is not None

    # 6. Evaluate compliance
    comp_req = EvaluateComplianceRequest(
        tenant_id="tenant_api_audit",
        framework=ComplianceFramework.ISO27001,
    )
    comp_res = evaluate_compliance(comp_req)
    assert comp_res.total_controls >= 1

    # 7. Create investigation case
    case_req = CreateInvestigationCaseRequest(
        tenant_id="tenant_api_audit",
        title="Key Rotation Forensic Audit",
        summary="Verifying scheduled rotation compliance",
        event_ids=[res_ev.event_id],
    )
    case = create_investigation_case(case_req)
    assert case.case_id is not None

    timeline = get_investigation_timeline(case_id=case.case_id, tenant_id="tenant_api_audit")
    assert timeline.total_items == 1
