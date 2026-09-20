"""Tests for Certification Transparency Log, Compliance Mapping Engine, and Dashboard Generator."""

import pytest
import json
from pathlib import Path
from enterprise_audit_engine.transparency.transparency_log import (
    CertificationTransparencyLog,
    TransparencyLogEntry,
)
from enterprise_audit_engine.compliance.compliance_mapper import (
    ComplianceMappingEngine,
    EnterpriseComplianceReport,
)
from enterprise_audit_engine.dashboard.dashboard_generator import (
    DashboardGenerator,
    AuditDashboard,
)


@pytest.fixture
def transparency_log(tmp_path):
    log_dir = tmp_path / "transparency"
    return CertificationTransparencyLog(log_dir)


def test_transparency_log_append_and_load(transparency_log):
    entry1 = transparency_log.append_entry(
        certificate_id="CERT-001",
        release_version="1.0.0",
        merkle_root="root_hash_001",
        issuer="Audit CA",
        status="VALID",
    )
    assert isinstance(entry1, TransparencyLogEntry)
    assert entry1.entry_id == 1
    assert len(entry1.entry_hash) == 64

    entry2 = transparency_log.append_entry(
        certificate_id="CERT-002",
        release_version="1.1.0",
        merkle_root="root_hash_002",
        issuer="Audit CA",
        status="VALID",
    )
    assert entry2.entry_id == 2
    assert entry2.prev_entry_hash == entry1.entry_hash

    entries = transparency_log.load_entries()
    assert len(entries) == 2
    assert entries[0].certificate_id == "CERT-001"
    assert entries[1].certificate_id == "CERT-002"


def test_transparency_log_integrity_verification_valid(transparency_log):
    transparency_log.append_entry("CERT-001", "1.0.0", "root1", "CA", "VALID")
    transparency_log.append_entry("CERT-002", "1.1.0", "root2", "CA", "VALID")
    transparency_log.append_entry("CERT-003", "1.2.0", "root3", "CA", "VALID")

    res = transparency_log.verify_log_integrity()
    assert res["is_valid"] is True
    assert res["entries_count"] == 3
    assert res["tampered_count"] == 0
    assert res["status"] == "CHAIN_VALID_AND_TAMPER_FREE"


def test_transparency_log_tamper_detection(transparency_log):
    transparency_log.append_entry("CERT-001", "1.0.0", "root1", "CA", "VALID")
    transparency_log.append_entry("CERT-002", "1.1.0", "root2", "CA", "VALID")

    # Tamper with the raw log file
    lines = transparency_log.log_file.read_text(encoding="utf-8").strip().split("\n")
    tampered_entry = json.loads(lines[0])
    tampered_entry["merkle_root"] = "TAMPERED_ROOT"
    lines[0] = json.dumps(tampered_entry)
    transparency_log.log_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    res = transparency_log.verify_log_integrity()
    assert res["is_valid"] is False
    assert res["tampered_count"] > 0
    assert res["status"] == "CHAIN_INTEGRITY_COMPROMISED"


def test_compliance_mapping_engine_evaluation():
    engine = ComplianceMappingEngine()
    evidence_items = [
        {"id": "EV-1", "category": "SecurityAndCompliance", "name": "Bandit AST Scan"},
        {"id": "EV-2", "category": "AutomatedTesting", "name": "Pytest Suite 100% Pass"},
        {"id": "EV-3", "category": "GitProvenanceAndIdentity", "name": "Signed Git Commit"},
        {"id": "EV-4", "category": "RuntimeExecutionAndHealth", "name": "Live Health Endpoint Check"},
        {"id": "EV-5", "category": "DependencyHygieneAndSBOM", "name": "Locked Pipfile & CycloneDX"},
        {"id": "EV-6", "category": "CryptographicCertificationSeal", "name": "Ed25519 Signed Merkle Root"},
    ]

    report = engine.evaluate_compliance(evidence_items, target_release="v1.0.0")
    assert isinstance(report, EnterpriseComplianceReport)
    assert report.total_frameworks_evaluated >= 4
    assert report.overall_compliance_score >= 80.0
    assert "OWASP_ASVS_V4" in report.framework_reports
    assert "SLSA_LEVEL_3" in report.framework_reports
    assert "ISO_IEC_25010" in report.framework_reports
    assert "SOC_2_TYPE_II" in report.framework_reports


def test_dashboard_generator(tmp_path):
    gen = DashboardGenerator(tmp_path)
    dashboard = gen.generate_dashboard(
        target_release="v1.0.0",
        engine_version="2.1.0",
        integrity_data={"is_valid": True, "hash": "abc"},
        baseline_data={"matched": True},
        mutation_data={"mutations_blocked_count": 50, "total_mutations_executed": 50},
        transparency_data={"is_valid": True},
        compliance_data={"overall_compliance_score": 95.0},
        reproducibility_data={"is_deterministic": True},
    )

    assert isinstance(dashboard, AuditDashboard)
    assert dashboard.summary.overall_certification_status == "CERTIFIED"
    assert dashboard.summary.trust_assurance_score == 100.0
    assert (tmp_path / "audit_dashboard.json").exists()
