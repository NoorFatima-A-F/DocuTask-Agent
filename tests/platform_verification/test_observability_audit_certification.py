"""
Phase 3H.4.12: Enterprise Observability Evidence, Audit & Certification Test Suite
"""
import os
import json
import pytest
from app.platform_verification.observability_audit_certification.verifiers import (
    EvidenceCollectionArchitectureVerifier,
    EvidenceIntegrityVerifier,
    ObservabilityAuditTrailVerifier,
    ProductionReadinessReviewer,
    ObservabilityComplianceValidator,
    ObservabilityCertificationEngine,
    CICDVerificationGate,
)
from app.platform_verification.observability_audit_certification.runtime.observability_audit_certification_runtime import (
    ObservabilityAuditCertificationRuntime,
)
from app.platform_verification.observability_audit_certification.domain.models import (
    CertificationTier,
    CICDDecision,
)


class TestObservabilityAuditCertification:
    def test_evidence_collection_architecture(self):
        """3H.4.12.1: Verify automated evidence collection across 8 source categories."""
        verifier = EvidenceCollectionArchitectureVerifier()
        report = verifier.verify_collection_architecture()

        assert report.is_fully_automated is True
        assert report.total_sources_covered == 8
        assert report.evidence_manifest_count >= 15
        assert len(report.manifests) >= 15
        for m in report.manifests:
            assert m.is_valid is True
            assert len(m.sha256_hash) == 64

    def test_evidence_integrity_verification_sha256(self):
        """3H.4.12.2: Verify SHA-256 cryptographic hashing, immutability, and tamper resistance."""
        arch_verifier = EvidenceCollectionArchitectureVerifier()
        arch_report = arch_verifier.verify_collection_architecture()

        integrity_verifier = EvidenceIntegrityVerifier()
        integrity_report = integrity_verifier.verify_evidence_integrity([m.model_dump() for m in arch_report.manifests])

        assert integrity_report.all_hashes_matched is True
        assert integrity_report.tamper_resistance_verified is True
        assert integrity_report.total_files_audited == len(arch_report.manifests)
        assert integrity_report.generator_version is not None

    def test_observability_audit_trail_events(self):
        """3H.4.12.3: Verify complete audit trail log with timestamps, actors, and test IDs."""
        verifier = ObservabilityAuditTrailVerifier()
        report = verifier.generate_audit_trail()

        assert report.audit_trail_immutable is True
        assert report.total_events >= 8
        for evt in report.audit_events:
            assert evt.event_id.startswith("evt-")
            assert evt.result in ["SUCCESS", "PASSED", "SEALED"]

    def test_production_readiness_review_prr(self):
        """3H.4.12.4: Verify PRR evaluation across 6 operational categories."""
        reviewer = ProductionReadinessReviewer()
        report = reviewer.execute_prr_review()

        assert report.overall_prr_score == 100.0
        assert report.prr_status == "APPROVED"
        assert report.signoff_approved is True
        assert len(report.categories) == 6

    def test_observability_compliance_validation(self):
        """3H.4.12.5: Verify compliance matrix against OpenTelemetry, Prometheus, OWASP, and NIST."""
        validator = ObservabilityComplianceValidator()
        report = validator.validate_compliance()

        assert report.compliance_passed is True
        assert report.compliance_percentage == 100.0
        assert report.total_rules_evaluated >= 6
        for item in report.compliance_matrix:
            assert item.status == "COMPLIANT"

    def test_observability_certification_engine_scoring(self):
        """3H.4.12.6: Verify 9-category weighted certification scoring model."""
        reviewer = ProductionReadinessReviewer()
        validator = ObservabilityComplianceValidator()
        arch_verifier = EvidenceCollectionArchitectureVerifier()
        integrity_verifier = EvidenceIntegrityVerifier()

        prr = reviewer.execute_prr_review()
        comp = validator.validate_compliance()
        arch = arch_verifier.verify_collection_architecture()
        integrity = integrity_verifier.verify_evidence_integrity([m.model_dump() for m in arch.manifests])

        engine = ObservabilityCertificationEngine()
        cert = engine.calculate_certification(prr, comp, integrity)

        assert cert.composite_score >= 95.0
        assert cert.certification_tier == CertificationTier.ENTERPRISE_CERTIFIED
        assert cert.certified is True
        assert len(cert.category_scores) == 9

    def test_cicd_verification_deployment_gate(self):
        """3H.4.12.7: Verify CI/CD automated deployment approval logic."""
        reviewer = ProductionReadinessReviewer()
        validator = ObservabilityComplianceValidator()
        arch_verifier = EvidenceCollectionArchitectureVerifier()
        integrity_verifier = EvidenceIntegrityVerifier()
        engine = ObservabilityCertificationEngine()
        gate = CICDVerificationGate()

        prr = reviewer.execute_prr_review()
        comp = validator.validate_compliance()
        arch = arch_verifier.verify_collection_architecture()
        integrity = integrity_verifier.verify_evidence_integrity([m.model_dump() for m in arch.manifests])
        cert = engine.calculate_certification(prr, comp, integrity)

        gate_res = gate.evaluate_deployment_gate(cert)
        assert gate_res.gate_decision == CICDDecision.DEPLOY
        assert gate_res.pipeline_exit_code == 0
        assert gate_res.hard_gates_passed is True

    def test_standardized_evidence_repository_export(self, tmp_path):
        """3H.4.12.8 & 3H.4.12.9: Verify export to standardized repository directory."""
        runtime = ObservabilityAuditCertificationRuntime()
        out_dir = str(tmp_path / "observability_certification")
        results = runtime.run_full_audit_and_certification(output_dir=out_dir)

        expected_dirs = [
            "health",
            "metrics",
            "dashboards",
            "alerts",
            "incidents",
            "failure_tests",
            "audit",
            "certification",
        ]
        for ed in expected_dirs:
            assert os.path.isdir(os.path.join(out_dir, ed))

        expected_files = [
            "evidence_collection_architecture.json",
            "evidence_integrity_report.json",
            "audit_trail_report.json",
            "production_readiness_review.json",
            "observability_compliance_report.json",
            "certification_report.json",
            "cicd_gate_report.json",
            "metadata.json",
            "certification_summary.md",
        ]
        for ef in expected_files:
            p = os.path.join(out_dir, ef)
            assert os.path.exists(p), f"Missing root manifest: {ef}"

    def test_certification_summary_markdown_report(self, tmp_path):
        """3H.4.12.10: Verify certification_summary.md contents and signoff."""
        runtime = ObservabilityAuditCertificationRuntime()
        out_dir = str(tmp_path / "observability_certification")
        runtime.run_full_audit_and_certification(output_dir=out_dir)

        summary_file = os.path.join(out_dir, "certification_summary.md")
        assert os.path.exists(summary_file)
        with open(summary_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Enterprise Observability Certification Summary" in content
            assert "Enterprise Certified" in content
            assert "Production Readiness Review (PRR) Signoff" in content
