"""Tests for Compliance Framework Controls and Compliance Assessment Engine."""

from app.audit.compliance.frameworks import ComplianceFramework
from app.audit.compliance.controls import DEFAULT_COMPLIANCE_CONTROLS
from app.audit.compliance.mappings import ComplianceAssessmentEngine
from app.audit.storage.repository import AuditRepository
from app.audit.evidence.manager import EvidenceManager
from app.audit.evidence.artifacts import EvidenceType
from app.audit.core.events import AuditEvent, EventCategory


def test_compliance_frameworks_definitions():
    assert len(DEFAULT_COMPLIANCE_CONTROLS) >= 6
    frameworks = {c.framework for c in DEFAULT_COMPLIANCE_CONTROLS}
    assert ComplianceFramework.SOC2 in frameworks
    assert ComplianceFramework.EU_AI_ACT in frameworks
    assert ComplianceFramework.NIST_AI_RMF in frameworks


def test_compliance_evaluation_engine_with_evidence():
    repo = AuditRepository()
    evidence_mgr = EvidenceManager(repository=repo)
    engine = ComplianceAssessmentEngine(repository=repo, evidence_manager=evidence_mgr)

    tenant_id = "tenant_soc2_test"

    # Ingest SOC2 CC7.2 (Security Monitoring) & CC6.1 (Logical Access) matching events and artifacts
    repo.record(
        AuditEvent(
            event_type="auth.login",
            category=EventCategory.AUTHENTICATION,
            tenant_id=tenant_id,
            actor_id="user_admin",
            action="login",
            resource_type="auth",
            resource_id="session",
        )
    )
    repo.record(
        AuditEvent(
            event_type="permission.grant",
            category=EventCategory.AUTHORIZATION,
            tenant_id=tenant_id,
            actor_id="user_admin",
            action="grant",
            resource_type="role",
            resource_id="developer",
        )
    )
    evidence_mgr.create_artifact(
        tenant_id=tenant_id,
        name="RBAC Policy Snapshot",
        evidence_type=EvidenceType.GOVERNANCE_EVIDENCE,
        source="policy_engine",
        content="{}",
    )

    report = engine.evaluate_compliance(tenant_id=tenant_id, framework=ComplianceFramework.SOC2)
    assert report.framework == ComplianceFramework.SOC2
    assert report.total_controls == 2
    assert report.overall_compliance_score >= 50.0
    assert report.compliant_controls >= 1
