"""Pytest Test Suite for Phase 3H.3.12 - Enterprise Readiness Evidence Generation & Audit Framework."""

import os
import json
import pytest
from app.platform_verification.readiness_audit_framework.domain.models import (
    EvidenceStatus,
    EvidenceSeverity,
    AuditCertificationTier,
)
from app.platform_verification.readiness_audit_framework.collector.readiness_evidence_collector import (
    ReadinessEvidenceCollector,
)
from app.platform_verification.readiness_audit_framework.schema.evidence_schema_normalizer import (
    EvidenceSchemaNormalizer,
)
from app.platform_verification.readiness_audit_framework.repository.evidence_repository_manager import (
    EvidenceRepositoryManager,
)
from app.platform_verification.readiness_audit_framework.metadata.evidence_metadata_generator import (
    EvidenceMetadataGenerator,
)
from app.platform_verification.readiness_audit_framework.integrity.evidence_integrity_verifier import (
    EvidenceIntegrityVerifier,
)
from app.platform_verification.readiness_audit_framework.timeline.readiness_timeline_reconstructor import (
    ReadinessTimelineReconstructor,
)
from app.platform_verification.readiness_audit_framework.failures.failure_evidence_documenter import (
    FailureEvidenceDocumenter,
)
from app.platform_verification.readiness_audit_framework.comparison.evidence_regression_comparator import (
    EvidenceRegressionComparator,
)
from app.platform_verification.readiness_audit_framework.observability.operational_dashboard_evidence_builder import (
    OperationalDashboardEvidenceBuilder,
)
from app.platform_verification.readiness_audit_framework.cicd.cicd_deployment_gate_evaluator import (
    CICDDeploymentGateEvaluator,
)
from app.platform_verification.readiness_audit_framework.scoring.evidence_quality_scorer import (
    EvidenceQualityScorer,
)
from app.platform_verification.readiness_audit_framework.package.final_evidence_package_generator import (
    FinalEvidencePackageGenerator,
)
from app.platform_verification.readiness_audit_framework.runtime.readiness_audit_runtime import (
    ReadinessAuditRuntime,
)
from app.platform_verification.readiness_audit_framework.api.readiness_audit_api import (
    get_audit_status,
    get_integrity_status,
    generate_evidence_package,
)


def test_readiness_evidence_collector():
    """Test 3H.3.12.1 - Evidence Collection Architecture."""
    collector = ReadinessEvidenceCollector()
    raw = collector.collect_raw_evidence()
    assert len(raw) >= 8
    components = {r["component"] for r in raw}
    assert "postgresql" in components
    assert "redis_queue" in components
    assert "worker_fleet" in components
    assert "gemini_ai" in components


def test_evidence_schema_normalizer():
    """Test 3H.3.12.2 - Universal Schema Normalization."""
    collector = ReadinessEvidenceCollector()
    normalizer = EvidenceSchemaNormalizer()
    records = normalizer.normalize_records(collector.collect_raw_evidence())

    assert len(records) >= 8
    for rec in records:
        assert rec.phase == "3H.3"
        assert rec.status == EvidenceStatus.PASS
        assert rec.severity in (EvidenceSeverity.INFO, EvidenceSeverity.LOW, EvidenceSeverity.MEDIUM)
        assert isinstance(rec.metrics, dict)
        assert len(rec.logs) > 0


def test_evidence_repository_manager(tmp_path):
    """Test 3H.3.12.3 - Readiness Evidence Repository."""
    repo = EvidenceRepositoryManager(base_dir=str(tmp_path))
    run_dir = repo.create_run_directory()
    assert os.path.exists(run_dir)
    assert os.path.exists(repo.get_base_directory())


def test_evidence_metadata_generator():
    """Test 3H.3.12.4 - Automated Metadata Generation."""
    gen = EvidenceMetadataGenerator()
    meta = gen.generate_metadata()
    assert meta.project == "DocuTask-Agent"
    assert meta.phase == "3H.3.12"
    assert meta.environment == "production-simulation"
    assert len(meta.commit) > 0
    assert len(meta.python_version) > 0


def test_readiness_timeline_reconstructor():
    """Test 3H.3.12.6 - Timeline Reconstruction & TTR."""
    recon = ReadinessTimelineReconstructor()
    rep = recon.reconstruct_timeline()

    assert rep.time_to_ready_seconds <= 5.0
    assert rep.recovery_time_seconds > 0.0
    assert rep.ttr_compliant is True
    assert len(rep.events) == 6
    assert rep.events[-1].state_after == "READY"


def test_failure_evidence_documenter():
    """Test 3H.3.12.7 - Failure Evidence Documentation."""
    doc = FailureEvidenceDocumenter()
    rep = doc.document_failures()

    assert rep.total_failures_tested == 4
    assert rep.all_recoveries_validated is True
    for f in rep.failure_records:
        assert f.result == EvidenceStatus.PASS
        assert len(f.readiness_transitions) >= 3


def test_evidence_regression_comparator():
    """Test 3H.3.12.8 - Evidence Comparison & Regression Engine."""
    comp = EvidenceRegressionComparator()
    rep = comp.compare_against_baseline()

    assert rep.baseline_version == "1.0.0"
    assert rep.current_version == "1.1.0"
    assert len(rep.comparisons) == 4
    assert rep.regression_found is False


def test_operational_dashboard_evidence_builder():
    """Test 3H.3.12.9 - Operational Dashboard Evidence."""
    builder = OperationalDashboardEvidenceBuilder()
    dash = builder.build_dashboard_evidence()

    assert dash["current_readiness_state"] == "READY"
    assert dash["historical_availability_pct"] >= 99.9
    assert dash["dependency_reliability"]["postgresql"]["uptime_pct"] >= 99.9


def test_cicd_deployment_gate_evaluator():
    """Test 3H.3.12.10 - CI/CD Deployment Gate Evaluation."""
    runtime = ReadinessAuditRuntime()
    res = runtime.run_full_audit()
    evaluator = CICDDeploymentGateEvaluator()

    gate = evaluator.evaluate_gate(res["scorecard"], len(res["manifests"]))
    assert gate["deployment_gate_decision"] == "APPROVED"
    assert gate["passed"] is True
    assert gate["score"] >= 95.0


def test_evidence_quality_scorer():
    """Test 3H.3.12.11 - Evidence Quality Scoring."""
    runtime = ReadinessAuditRuntime()
    res = runtime.run_full_audit()
    scorecard = res["scorecard"]

    assert scorecard.overall_score >= 95.0
    assert scorecard.certification_tier == AuditCertificationTier.ENTERPRISE_EVIDENCE_CERTIFIED
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.passed is True


def test_final_evidence_package_generator(tmp_path):
    """Test 3H.3.12.12 - Final Evidence Package Generation (13 JSONs + README.md)."""
    runtime = ReadinessAuditRuntime(export_dir=str(tmp_path))
    res = runtime.run_full_audit()
    manifests = res["manifests"]

    expected_files = [
        "metadata.json",
        "readiness_contract_report.json",
        "dependency_report.json",
        "database_report.json",
        "queue_report.json",
        "worker_report.json",
        "ai_provider_report.json",
        "startup_report.json",
        "failure_report.json",
        "recovery_report.json",
        "metrics_report.json",
        "integrity_report.json",
        "certification_report.json",
        "README.md",
    ]

    assert len(manifests) == 14
    for fname in expected_files:
        assert fname in manifests
        fpath = manifests[fname]
        assert os.path.exists(fpath)
        if fname.endswith(".json"):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)


def test_evidence_integrity_verifier(tmp_path):
    """Test 3H.3.12.5 - SHA-256 Checksums and Integrity Verification."""
    runtime = ReadinessAuditRuntime(export_dir=str(tmp_path))
    res = runtime.run_full_audit()
    integrity = res["integrity_report"]

    assert integrity.total_artifacts_hashed >= 12
    assert integrity.all_hashes_verified is True
    assert integrity.tampering_detected is False


def test_readiness_audit_api_endpoints():
    """Test FastAPI router endpoints."""
    status = get_audit_status()
    assert status["status"] == "HEALTHY"
    assert status["cicd_decision"]["passed"] is True

    integ = get_integrity_status()
    assert integ["all_hashes_verified"] is True

    pkg = generate_evidence_package()
    assert pkg["scorecard"]["passed"] is True
    assert len(pkg["manifests_generated"]) == 14
