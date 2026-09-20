"""
Phase 3P: Comprehensive Test Suite for Enterprise Verification Evidence Intelligence System.
"""

import json
import os
from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_evidence_intelligence.domain.models import (
    ComplianceReport,
    DeploymentBadge,
    EngineeringAuditReport,
    EvidenceChain,
    EvidenceProvenance,
    EvidenceSeverity,
    EvidenceStatus,
    ExecutiveCertificationReport,
    FailureEvidenceItem,
    FailureEvidenceReport,
    PortfolioEvidenceBundle,
    StandardizedEvidenceItem,
    VerificationManifest,
)
from app.platform_verification.enterprise_evidence_intelligence.collectors import (
    ChaosEvidenceCollector,
    CloudEvidenceCollector,
    ContainerEvidenceCollector,
    DeploymentEvidenceCollector,
    ObservabilityEvidenceCollector,
    PerformanceEvidenceCollector,
    RecoveryEvidenceCollector,
    SecurityEvidenceCollector,
)
from app.platform_verification.enterprise_evidence_intelligence.validators.evidence_validator import (
    EvidenceValidator,
)
from app.platform_verification.enterprise_evidence_intelligence.compliance.compliance_mapper import (
    ComplianceMapper,
)
from app.platform_verification.enterprise_evidence_intelligence.failure.failure_evidence_manager import (
    FailureEvidenceManager,
)
from app.platform_verification.enterprise_evidence_intelligence.reporters import (
    EngineeringAuditGenerator,
    ExecutiveReportGenerator,
    PortfolioLayerGenerator,
)
from app.platform_verification.enterprise_evidence_intelligence.exporter.evidence_intelligence_exporter import (
    EvidenceIntelligenceExporter,
)
from app.platform_verification.enterprise_evidence_intelligence.runtime.evidence_intelligence_runtime import (
    EvidenceIntelligenceRuntime,
)
from app.platform_verification.enterprise_evidence_intelligence.api.evidence_intelligence_api import (
    router,
)


class TestEnterpriseEvidenceIntelligence:
    """Complete test suite for Phase 3P."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_evidence_platform"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Collectors Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_container_collector(self):
        collector = ContainerEvidenceCollector()
        items = collector.collect()
        assert len(items) == 3
        assert all(it.category == "Container Architecture" for it in items)
        assert items[0].id == "EV-CONT-001"
        assert items[0].metrics["user_uid"] == 10001

    def test_security_collector(self):
        collector = SecurityEvidenceCollector()
        items = collector.collect()
        assert len(items) == 4
        assert all(it.category == "Security" for it in items)
        assert any(it.type == "vulnerability_scan" for it in items)
        assert any(it.type == "ai_security" for it in items)

    def test_performance_collector(self):
        collector = PerformanceEvidenceCollector()
        items = collector.collect()
        assert len(items) == 3
        assert any(it.type == "latency_benchmark" for it in items)
        assert any(it.type == "throughput_capacity" for it in items)

    def test_chaos_collector(self):
        collector = ChaosEvidenceCollector()
        items = collector.collect()
        assert len(items) == 3
        assert all(it.category == "Reliability" for it in items)
        assert items[0].metrics["recovery_time_seconds"] <= 5.0

    def test_recovery_collector(self):
        collector = RecoveryEvidenceCollector()
        items = collector.collect()
        assert len(items) == 3
        assert all(it.category == "Recovery Capability" for it in items)
        assert items[0].metrics["observed_rto_minutes"] <= 15.0

    def test_observability_collector(self):
        collector = ObservabilityEvidenceCollector()
        items = collector.collect()
        assert len(items) == 3
        assert any(it.type == "distributed_tracing" for it in items)

    def test_deployment_and_cloud_collectors(self):
        dep_collector = DeploymentEvidenceCollector()
        dep_items = dep_collector.collect()
        assert len(dep_items) == 2

        cloud_collector = CloudEvidenceCollector()
        cloud_items = cloud_collector.collect()
        assert len(cloud_items) == 1

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Validator Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_evidence_validator_valid_and_invalid(self):
        validator = EvidenceValidator()
        valid_item = StandardizedEvidenceItem(
            id="EV-TEST-001",
            type="unit_test",
            category="Testing",
            component="test_service",
            test_name="Sanity Test",
            metrics={"passed": True},
            artifacts=["report.json"],
        )
        assert validator.validate(valid_item) is True

        invalid_item = StandardizedEvidenceItem(
            id="INVALID-PREFIX",
            type="unit_test",
            category="Testing",
            component="",
            test_name="",
        )
        assert validator.validate(invalid_item) is False

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Compliance Mapping Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_compliance_mapper_standards(self):
        runtime = EvidenceIntelligenceRuntime()
        res = runtime.run_full_pipeline()
        comp: ComplianceReport = res["compliance"]

        assert len(comp.soc2_controls) >= 4
        assert len(comp.iso27001_controls) >= 3
        assert len(comp.nist_controls) >= 3
        assert comp.overall_compliance_pct == 100.0
        assert all(c.status == "COMPLIANT" for c in comp.soc2_controls)

    # ──────────────────────────────────────────────────────────────────────────
    # 4. Failure Intelligence Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_failure_manager_clean_and_failure(self):
        manager = FailureEvidenceManager()
        clean_items = [
            StandardizedEvidenceItem(
                id="EV-PASS-001",
                type="pass",
                category="Reliability",
                component="comp1",
                test_name="test1",
                status=EvidenceStatus.PASS,
            )
        ]
        report = manager.analyze_failures(clean_items)
        assert report.failures_detected == 0

        failed_items = [
            StandardizedEvidenceItem(
                id="EV-FAIL-001",
                type="chaos_fail",
                category="Reliability",
                component="worker_pool",
                test_name="Worker Recovery Timeout",
                status=EvidenceStatus.FAIL,
                severity=EvidenceSeverity.HIGH,
                details="Worker resurrection exceeded 15s deadline",
            )
        ]
        fail_report = manager.analyze_failures(failed_items)
        assert fail_report.failures_detected == 1
        assert fail_report.high_failures_count == 1
        assert len(fail_report.failures[0].reproduction_steps) > 0
        assert len(fail_report.failures[0].recommendation) > 0

    # ──────────────────────────────────────────────────────────────────────────
    # 5. Dual Reports & Portfolio Layer Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_executive_and_engineering_reports(self):
        runtime = EvidenceIntelligenceRuntime()
        res = runtime.run_full_pipeline()

        exec_rep: ExecutiveCertificationReport = res["executive_report"]
        assert exec_rep.score == 100.0
        assert exec_rep.critical_failures == 0
        assert len(exec_rep.verified_pillars) >= 7

        audit_rep: EngineeringAuditReport = res["audit_report"]
        assert len(audit_rep.topology["services"]) >= 5
        assert audit_rep.performance_benchmarks["p95_latency_ms"] < 100.0

    def test_portfolio_layer_bundle(self):
        runtime = EvidenceIntelligenceRuntime()
        res = runtime.run_full_pipeline()

        portfolio: PortfolioEvidenceBundle = res["portfolio"]
        assert portfolio.score == 100.0
        assert "Reliability" in portfolio.reliability_summary
        assert "Zero-Trust" in portfolio.security_summary
        assert portfolio.badge.label == "Infrastructure"
        assert portfolio.badge.message == "Enterprise Ready (100%)"

    # ──────────────────────────────────────────────────────────────────────────
    # 6. Exporter, Cryptographic Chaining & Manifest Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_exporter_cryptographic_chain(self, temp_export_dir):
        runtime = EvidenceIntelligenceRuntime()
        res = runtime.run_full_pipeline(export_dir=temp_export_dir)

        base = Path(temp_export_dir)
        assert (base / "evidence" / "standardized_evidence.json").exists()
        assert (base / "reports" / "compliance_mapping.json").exists()
        assert (base / "reports" / "executive_certification_report.md").exists()
        assert (base / "reports" / "engineering_audit_report.md").exists()
        assert (base / "artifacts" / "final_certification.json").exists()
        assert (base / "artifacts" / "container_report.json").exists()
        assert (base / "metadata" / "provenance.json").exists()
        assert (base / "hashes" / "evidence_chain.json").exists()
        assert (base / "portfolio_evidence" / "deployment_badge.json").exists()
        assert (base / "metadata.json").exists()
        assert (base / "manifest.json").exists()

        # Verify evidence chain
        with open(base / "hashes" / "evidence_chain.json", "r", encoding="utf-8") as f:
            chain_data = json.load(f)
            assert chain_data["chain_id"] == "CHAIN-3P-VERIFY-001"
            assert len(chain_data["records"]) > 10
            assert len(chain_data["head_hash"]) == 64

        manifest: VerificationManifest = res["manifest"]
        assert manifest.overall_score == 100.0
        assert manifest.deployment_approved is True
        for fentry in manifest.files:
            assert len(fentry.sha256) == 64
            assert fentry.size_bytes > 0

    # ──────────────────────────────────────────────────────────────────────────
    # 7. FastAPI REST API Endpoints Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health(self, app_client):
        res = app_client.get("/api/v1/evidence/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"

    def test_api_provenance(self, app_client):
        res = app_client.get("/api/v1/evidence/provenance")
        assert res.status_code == 200
        data = res.json()
        assert data["repository"] == "DocuTask-Agent"
        assert len(data["commit_hash"]) == 40

    def test_api_items(self, app_client):
        res = app_client.get("/api/v1/evidence/items")
        assert res.status_code == 200
        data = res.json()
        assert len(data) >= 15
        assert data[0]["id"].startswith("EV-")

    def test_api_compliance(self, app_client):
        res = app_client.get("/api/v1/evidence/compliance")
        assert res.status_code == 200
        data = res.json()
        assert data["overall_compliance_pct"] == 100.0

    def test_api_failures(self, app_client):
        res = app_client.get("/api/v1/evidence/failures")
        assert res.status_code == 200
        data = res.json()
        assert data["critical_failures_count"] == 0

    def test_api_executive_and_audit(self, app_client):
        res = app_client.get("/api/v1/evidence/executive")
        assert res.status_code == 200
        assert res.json()["score"] == 100.0

        res_audit = app_client.get("/api/v1/evidence/audit")
        assert res_audit.status_code == 200
        assert "FastAPI Gateway" in res_audit.json()["topology"]["services"]

    def test_api_portfolio(self, app_client):
        res = app_client.get("/api/v1/evidence/portfolio")
        assert res.status_code == 200
        data = res.json()
        assert data["score"] == 100.0
        assert data["badge"]["label"] == "Infrastructure"

    def test_api_run_and_manifest(self, app_client):
        res = app_client.post("/api/v1/evidence/run")
        assert res.status_code == 200
        manifest = res.json()
        assert manifest["overall_score"] == 100.0
        assert manifest["deployment_approved"] is True

        res_man = app_client.get("/api/v1/evidence/manifest")
        assert res_man.status_code == 200
        assert len(res_man.json()["files"]) > 0

    def test_api_markdown_endpoints(self, app_client):
        res_exec = app_client.get("/api/v1/evidence/reports/executive/markdown")
        assert res_exec.status_code == 200
        assert "Executive Infrastructure Certification Report" in res_exec.text

        res_audit = app_client.get("/api/v1/evidence/reports/audit/markdown")
        assert res_audit.status_code == 200
        assert "Deep-Dive Engineering Infrastructure Audit Report" in res_audit.text
