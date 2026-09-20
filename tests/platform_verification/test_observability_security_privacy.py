"""
Test Suite: Phase 3I.7 Observability Security, Privacy & Compliance Verification Framework
"""
import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.observability_security.domain.models import (
    SecurityCertificationTier,
    ThreatSeverity,
    RBACRole,
    ObservabilityThreatModelReport,
    SensitiveDataReport,
    LogRedactionReport,
    AITelemetryPrivacyReport,
    AccessControlReport,
    TelemetryEncryptionReport,
    TelemetryRetentionReport,
    ObservabilityAuditReport,
    ComplianceMappingReport,
    AttackSimulationReport,
    TelemetryIncidentResponseReport,
    ContinuousSecurityReport,
    ObservabilitySecurityCertificationReport,
)

from app.platform_verification.observability_security.verifiers.threat_model_verifier import (
    ThreatModelVerifier,
)
from app.platform_verification.observability_security.verifiers.sensitive_data_verifier import (
    SensitiveDataVerifier,
)
from app.platform_verification.observability_security.verifiers.log_redaction_verifier import (
    LogRedactionVerifier,
)
from app.platform_verification.observability_security.verifiers.ai_privacy_verifier import (
    AIPrivacyVerifier,
)
from app.platform_verification.observability_security.verifiers.access_control_verifier import (
    AccessControlVerifier,
)
from app.platform_verification.observability_security.verifiers.telemetry_encryption_verifier import (
    TelemetryEncryptionVerifier,
)
from app.platform_verification.observability_security.verifiers.data_retention_verifier import (
    DataRetentionVerifier,
)
from app.platform_verification.observability_security.verifiers.audit_trail_verifier import (
    AuditTrailVerifier,
)
from app.platform_verification.observability_security.verifiers.compliance_mapping_verifier import (
    ComplianceMappingVerifier,
)
from app.platform_verification.observability_security.verifiers.attack_simulation_verifier import (
    AttackSimulationVerifier,
)
from app.platform_verification.observability_security.verifiers.incident_response_verifier import (
    IncidentResponseVerifier,
)
from app.platform_verification.observability_security.verifiers.continuous_security_verifier import (
    ContinuousSecurityVerifier,
)
from app.platform_verification.observability_security.scoring.observability_security_scorer import (
    ObservabilitySecurityScorer,
)
from app.platform_verification.observability_security.exporter.observability_security_evidence_exporter import (
    ObservabilitySecurityEvidenceExporter,
)
from app.platform_verification.observability_security.runtime.observability_security_runtime import (
    ObservabilitySecurityRuntime,
)
from app.platform_verification.observability_security.api.observability_security_api import (
    router as security_router,
)


# ─── 1. Individual Verifier Tests ─────────────────────────────────────────────

def test_threat_model_verifier():
    verifier = ThreatModelVerifier()
    report = verifier.verify_threat_model()

    assert isinstance(report, ObservabilityThreatModelReport)
    assert report.risks_identified >= 15
    assert report.critical_risks_unmitigated == 0
    assert len(report.threats) >= 5
    assert report.status == "PASS"


def test_sensitive_data_verifier():
    verifier = SensitiveDataVerifier()
    report = verifier.verify_sensitive_data_protection()

    assert isinstance(report, SensitiveDataReport)
    assert len(report.scans) == 3
    assert report.zero_sensitive_data_leaked is True
    assert report.status == "PASS"


def test_log_redaction_verifier():
    verifier = LogRedactionVerifier()
    report = verifier.verify_log_redaction()

    assert isinstance(report, LogRedactionReport)
    assert len(report.rules_applied) >= 5
    assert report.all_rules_verified is True
    assert report.redaction_pipeline_active is True

    rule_types = {r.pattern_type for r in report.rules_applied}
    assert "API_KEY" in rule_types
    assert "JWT" in rule_types
    assert "CNIC" in rule_types
    assert "EMAIL" in rule_types
    assert "DOCUMENT_TEXT" in rule_types


def test_ai_privacy_verifier():
    verifier = AIPrivacyVerifier()
    report = verifier.verify_ai_telemetry_privacy()

    assert isinstance(report, AITelemetryPrivacyReport)
    assert len(report.privacy_checks) >= 6
    assert report.prompts_and_responses_protected is True
    assert report.metadata_only_logging_enforced is True


def test_access_control_verifier():
    verifier = AccessControlVerifier()
    report = verifier.verify_access_control()

    assert isinstance(report, AccessControlReport)
    assert len(report.role_policies) == 4
    assert report.rbac_enforced is True
    assert report.mfa_mandatory_for_admins is True


def test_telemetry_encryption_verifier():
    verifier = TelemetryEncryptionVerifier()
    report = verifier.verify_telemetry_encryption()

    assert isinstance(report, TelemetryEncryptionReport)
    assert len(report.scopes) >= 5
    assert report.all_telemetry_encrypted is True


def test_data_retention_verifier():
    verifier = DataRetentionVerifier()
    report = verifier.verify_data_retention()

    assert isinstance(report, TelemetryRetentionReport)
    assert len(report.policies) >= 5
    assert report.lifecycle_management_active is True


def test_audit_trail_verifier():
    verifier = AuditTrailVerifier()
    report = verifier.verify_audit_trail()

    assert isinstance(report, ObservabilityAuditReport)
    assert len(report.sample_audit_events) >= 4
    assert report.audit_logging_active is True
    assert report.immutability_verified is True


def test_compliance_mapping_verifier():
    verifier = ComplianceMappingVerifier()
    report = verifier.verify_compliance_mapping()

    assert isinstance(report, ComplianceMappingReport)
    assert len(report.standards) >= 5
    assert report.overall_compliance_pct == 100.0


def test_attack_simulation_verifier():
    verifier = AttackSimulationVerifier()
    report = verifier.verify_attack_simulations()

    assert isinstance(report, AttackSimulationReport)
    assert len(report.simulations) >= 4
    assert report.all_attacks_mitigated is True


def test_incident_response_verifier():
    verifier = IncidentResponseVerifier()
    report = verifier.verify_incident_response()

    assert isinstance(report, TelemetryIncidentResponseReport)
    assert len(report.containment_steps) >= 5
    assert report.total_containment_time_sec <= 60.0
    assert report.sla_compliant is True


def test_continuous_security_verifier():
    verifier = ContinuousSecurityVerifier()
    report = verifier.verify_continuous_security()

    assert isinstance(report, ContinuousSecurityReport)
    assert len(report.checks) >= 4
    assert report.ci_cd_gate_enforced is True


# ─── 2. Scorer Tests ──────────────────────────────────────────────────────────

def test_observability_security_scorer():
    runtime = ObservabilitySecurityRuntime()
    scorer = runtime.scorer

    cert = scorer.calculate_certification_score(
        threat_report=runtime.threat_verifier.verify_threat_model(),
        data_report=runtime.data_verifier.verify_sensitive_data_protection(),
        redact_report=runtime.redact_verifier.verify_log_redaction(),
        ai_report=runtime.ai_verifier.verify_ai_telemetry_privacy(),
        access_report=runtime.access_verifier.verify_access_control(),
        encrypt_report=runtime.encrypt_verifier.verify_telemetry_encryption(),
        retention_report=runtime.retention_verifier.verify_data_retention(),
        audit_report=runtime.audit_verifier.verify_audit_trail(),
        compliance_report=runtime.compliance_verifier.verify_compliance_mapping(),
        attack_report=runtime.attack_verifier.verify_attack_simulations(),
        incident_report=runtime.incident_verifier.verify_incident_response(),
        continuous_report=runtime.continuous_verifier.verify_continuous_security(),
    )

    assert isinstance(cert, ObservabilitySecurityCertificationReport)
    assert len(cert.pillar_scores) == 6
    assert cert.overall_score_pct >= 95.0
    assert cert.certification_granted is True
    assert cert.certification_tier == SecurityCertificationTier.ENTERPRISE_OBSERVABILITY_SECURE

    total_weight = sum(p.weight_pct for p in cert.pillar_scores)
    assert total_weight == 100.0


# ─── 3. Exporter & Artifact Verification ──────────────────────────────────────

def test_observability_security_evidence_exporter(tmp_path):
    output_dir = str(tmp_path / "security_test_export")
    runtime = ObservabilitySecurityRuntime(output_dir=output_dir)
    results = runtime.run_full_verification()

    assert results["status"] == "SUCCESS"
    assert os.path.exists(output_dir)

    expected_files = [
        "threat_model_report.json",
        "sensitive_data_report.json",
        "redaction_report.json",
        "ai_privacy_report.json",
        "access_control_report.json",
        "encryption_report.json",
        "retention_report.json",
        "audit_report.json",
        "compliance_report.json",
        "attack_simulation_report.json",
        "incident_response_report.json",
        "continuous_security_report.json",
        "certification_report.json",
        "metadata.json",
    ]

    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        assert os.path.exists(fpath), f"Missing artifact: {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert len(data) > 0


# ─── 4. REST API Endpoints ───────────────────────────────────────────────────

@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(security_router)
    return TestClient(app)


def test_api_run_verification(api_client):
    response = api_client.post("/api/v1/observability-security/run-verification")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["certification_granted"] is True
    assert data["overall_score_pct"] >= 95.0


def test_api_status(api_client):
    response = api_client.get("/api/v1/observability-security/status")
    assert response.status_code == 200
    data = response.json()
    assert data["certification_granted"] is True
    assert data["overall_score_pct"] >= 95.0
    assert len(data["pillar_scores"]) == 6


def test_api_privacy_audit(api_client):
    response = api_client.get("/api/v1/observability-security/privacy-audit")
    assert response.status_code == 200
    data = response.json()
    assert "sensitive_data_scan" in data
    assert "redaction_rules" in data
    assert "ai_telemetry_privacy" in data


def test_api_threat_model(api_client):
    response = api_client.get("/api/v1/observability-security/threat-model")
    assert response.status_code == 200
    data = response.json()
    assert "threat_model" in data
    assert "attack_simulations" in data
