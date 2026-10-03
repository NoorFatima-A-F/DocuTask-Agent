"""
Phase 3Q: Comprehensive Test Suite for Enterprise Continuous Infrastructure Verification & CI/CD Pipeline Assurance.
"""

from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_continuous_verification.domain.models import (
    GateDecision,
    PipelineStageStatus,
)
from app.platform_verification.enterprise_continuous_verification.core import (
    BuildVerifier,
    ChangeImpactAnalyzer,
    ChaosPipelineRunner,
    DisposableEnvManager,
    DriftDetector,
    IntegrationWorkflowRunner,
    PerformanceGateValidator,
    ReleaseGatekeeper,
    SecurityGateEngine,
)
from app.platform_verification.enterprise_continuous_verification.exporter.continuous_verification_exporter import (
    ContinuousVerificationExporter,
)
from app.platform_verification.enterprise_continuous_verification.runtime.continuous_verification_runtime import (
    ContinuousVerificationRuntime,
)
from app.platform_verification.enterprise_continuous_verification.api.continuous_verification_api import (
    router,
)


class TestEnterpriseContinuousVerification:
    """Comprehensive test suite for Phase 3Q CI/CD Continuous Infrastructure Verification."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_pipeline_evidence"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Change Impact Analyzer Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_change_impact_dockerfile(self):
        analyzer = ChangeImpactAnalyzer()
        report = analyzer.analyze_changes(["Dockerfile", "src/main.py"])
        assert "Container Runtime" in report.changed_components
        assert "container_verification" in report.required_test_suites
        assert "deployment_verification" in report.required_test_suites
        assert any("Dockerfile" in f for f in report.files_modified)

    def test_change_impact_docker_compose(self):
        analyzer = ChangeImpactAnalyzer()
        report = analyzer.analyze_changes(["docker-compose.yml"])
        assert "Container Runtime" in report.changed_components
        assert "container_verification" in report.required_test_suites
        assert "deployment_verification" in report.required_test_suites

    def test_change_impact_requirements(self):
        analyzer = ChangeImpactAnalyzer()
        report = analyzer.analyze_changes(["requirements.txt"])
        assert "Dependencies & Supply Chain" in report.changed_components
        assert "security_scan" in report.required_test_suites
        assert "vulnerability_verification" in report.required_test_suites

    def test_change_impact_worker_changes(self):
        analyzer = ChangeImpactAnalyzer()
        report = analyzer.analyze_changes(["app/workers/celery_app.py"])
        assert "Task Queue & Worker Engine" in report.changed_components
        assert "worker_resilience" in report.required_test_suites
        assert "chaos_test" in report.required_test_suites

    def test_change_impact_api_changes(self):
        analyzer = ChangeImpactAnalyzer()
        report = analyzer.analyze_changes(["app/api/v1/documents.py"])
        assert "FastAPI Gateway" in report.changed_components
        assert "performance_test" in report.required_test_suites

    def test_change_impact_default_full_run(self):
        analyzer = ChangeImpactAnalyzer()
        report = analyzer.analyze_changes(None)
        assert len(report.changed_components) >= 4
        assert len(report.required_test_suites) >= 4

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Build Verifier Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_build_verifier_deterministic_digest(self):
        verifier = BuildVerifier()
        report = verifier.verify_build()
        assert report.build_status == PipelineStageStatus.PASSED
        assert report.digest_sha256.startswith("sha256:")
        assert report.version == "3.19.0"
        assert report.build_duration_sec > 0

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Security Gate Engine Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_security_gate_pass_clean(self):
        engine = SecurityGateEngine()
        report = engine.evaluate_security(critical_cves=0, high_cves=0, secrets_found=0)
        assert report.gate_passed is True
        assert report.container_scan_status == PipelineStageStatus.PASSED
        assert report.secret_scan_status == PipelineStageStatus.PASSED
        assert report.critical_vulnerabilities == 0
        assert report.secrets_detected == 0
        assert len(report.blocking_reasons) == 0

    def test_security_gate_block_on_critical_cves(self):
        engine = SecurityGateEngine()
        report = engine.evaluate_security(critical_cves=2, high_cves=1, secrets_found=0)
        assert report.gate_passed is False
        assert report.container_scan_status == PipelineStageStatus.BLOCKED
        assert report.critical_vulnerabilities == 2
        assert len(report.blocking_reasons) > 0
        assert "Critical CVE" in report.blocking_reasons[0]

    def test_security_gate_block_on_secrets(self):
        engine = SecurityGateEngine()
        report = engine.evaluate_security(critical_cves=0, high_cves=0, secrets_found=1)
        assert report.gate_passed is False
        assert report.secret_scan_status == PipelineStageStatus.BLOCKED
        assert report.secrets_detected == 1
        assert "secret" in report.blocking_reasons[0].lower()

    # ──────────────────────────────────────────────────────────────────────────
    # 4. Disposable Test Environment Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_disposable_env_lifecycle(self):
        manager = DisposableEnvManager()
        report = manager.provision_and_test()
        assert "ephemeral" in report.environment_id.lower() or "disposable" in report.environment_id.lower()
        assert report.health_check_status == PipelineStageStatus.PASSED
        assert report.teardown_status == PipelineStageStatus.PASSED
        assert len(report.services_deployed) >= 4
        assert "postgres" in report.services_deployed
        assert "redis" in report.services_deployed

    # ──────────────────────────────────────────────────────────────────────────
    # 5. Integration Workflow Runner Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_integration_e2e_workflow(self):
        runner = IntegrationWorkflowRunner()
        report = runner.execute_e2e_workflow()
        assert report.upload_status == PipelineStageStatus.PASSED
        assert report.queue_dispatch_status == PipelineStageStatus.PASSED
        assert report.worker_processing_status == PipelineStageStatus.PASSED
        assert report.db_persistence_status == PipelineStageStatus.PASSED
        assert report.retrieval_status == PipelineStageStatus.PASSED
        assert report.data_consistency_verified is True
        assert report.end_to_end_duration_ms > 0

    # ──────────────────────────────────────────────────────────────────────────
    # 6. Performance Regression Gate Validator Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_performance_gate_pass_within_threshold(self):
        validator = PerformanceGateValidator()
        report = validator.validate_performance(current_p95_ms=45.0, baseline_p95_ms=40.0)
        assert report.status == PipelineStageStatus.PASSED
        assert report.threshold_exceeded is False
        assert report.regression_detected is False
        assert report.latency_increase_pct == pytest.approx(12.5, rel=1e-2)

    def test_performance_gate_block_on_regression(self):
        validator = PerformanceGateValidator()
        # +60% latency increase exceeds the 50% threshold
        report = validator.validate_performance(current_p95_ms=64.0, baseline_p95_ms=40.0)
        assert report.status == PipelineStageStatus.BLOCKED
        assert report.threshold_exceeded is True
        assert report.regression_detected is True
        assert report.latency_increase_pct == pytest.approx(60.0, rel=1e-2)

    # ──────────────────────────────────────────────────────────────────────────
    # 7. Chaos Pipeline Runner Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_chaos_pipeline_resilience(self):
        runner = ChaosPipelineRunner()
        report = runner.run_chaos_experiments()
        assert report.worker_failure_recovered is True
        assert report.db_failure_recovered is True
        assert report.queue_partition_recovered is True
        assert report.lost_jobs == 0
        assert report.resilience_passed is True
        assert report.status == PipelineStageStatus.PASSED

    # ──────────────────────────────────────────────────────────────────────────
    # 8. Drift Detector Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_drift_detector_zero_drift(self):
        detector = DriftDetector()
        report = detector.detect_drift(declared_count=28, actual_count=28)
        assert report.drift_detected is False
        assert report.drifted_resources == 0
        assert report.drift_severity == "NONE"
        assert report.status == PipelineStageStatus.PASSED

    def test_drift_detector_drift_detected(self):
        detector = DriftDetector()
        report = detector.detect_drift(declared_count=28, actual_count=24)
        assert report.drift_detected is True
        assert report.drifted_resources == 4
        assert report.drift_severity == "HIGH"
        assert report.status == PipelineStageStatus.BLOCKED

    # ──────────────────────────────────────────────────────────────────────────
    # 9. Release Gatekeeper Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_release_gatekeeper_approval(self):
        gatekeeper = ReleaseGatekeeper()
        analyzer = ChangeImpactAnalyzer()
        build = BuildVerifier()
        security = SecurityGateEngine()
        env = DisposableEnvManager()
        integration = IntegrationWorkflowRunner()
        perf = PerformanceGateValidator()
        chaos = ChaosPipelineRunner()
        drift = DriftDetector()

        gate_reports = {
            "change_impact": analyzer.analyze_changes(),
            "build": build.verify_build(),
            "security": security.evaluate_security(0, 0, 0),
            "env": env.provision_and_test(),
            "integration": integration.execute_e2e_workflow(),
            "performance": perf.validate_performance(42.0, 40.0),
            "chaos": chaos.run_chaos_experiments(),
            "drift": drift.detect_drift(28, 28),
        }

        decision = gatekeeper.evaluate_release(gate_reports)
        assert decision.decision == GateDecision.APPROVED
        assert decision.confidence_score == 100.0
        assert len(decision.blocking_reasons) == 0

        certificate = gatekeeper.issue_certificate(decision, gate_reports)
        assert certificate.certificate_id.startswith("CERT-3Q-")
        assert certificate.certification == "PRODUCTION READY"
        assert certificate.security == "PASS"

    def test_release_gatekeeper_block_on_failed_security_gate(self):
        gatekeeper = ReleaseGatekeeper()
        security = SecurityGateEngine()

        gate_reports = {
            "security": security.evaluate_security(critical_cves=1, high_cves=0, secrets_found=0),
        }

        decision = gatekeeper.evaluate_release(gate_reports)
        assert decision.decision == GateDecision.BLOCKED
        assert decision.confidence_score < 100.0
        assert len(decision.blocking_reasons) > 0

    # ──────────────────────────────────────────────────────────────────────────
    # 10. Continuous Verification Exporter Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_exporter_artifact_tree_and_sha256(self, temp_export_dir):
        exporter = ContinuousVerificationExporter(base_dir=temp_export_dir)
        analyzer = ChangeImpactAnalyzer()
        build_v = BuildVerifier()
        sec = SecurityGateEngine()
        env_m = DisposableEnvManager()
        integ = IntegrationWorkflowRunner()
        perf_v = PerformanceGateValidator()
        chaos_r = ChaosPipelineRunner()
        drift_d = DriftDetector()
        gk = ReleaseGatekeeper()

        change_report = analyzer.analyze_changes()
        build_report = build_v.verify_build()
        sec_report = sec.evaluate_security(0, 0, 0)
        env_report = env_m.provision_and_test()
        integ_report = integ.execute_e2e_workflow()
        perf_report = perf_v.validate_performance(42.0, 40.0)
        chaos_report = chaos_r.run_chaos_experiments()
        drift_report = drift_d.detect_drift(28, 28)

        reports = {
            "change_impact": change_report,
            "build": build_report,
            "security": sec_report,
            "env": env_report,
            "integration": integ_report,
            "performance": perf_report,
            "chaos": chaos_report,
            "drift": drift_report,
        }
        dec = gk.evaluate_release(reports)
        cert = gk.issue_certificate(dec, reports)

        manifest = exporter.export_all(
            change_impact=change_report,
            build=build_report,
            security=sec_report,
            disposable_env=env_report,
            integration=integ_report,
            performance=perf_report,
            chaos=chaos_report,
            drift=drift_report,
            decision=dec,
            certificate=cert,
            export_dir=temp_export_dir,
        )

        assert manifest.deployment_approved is True
        assert len(manifest.files) >= 8

        # Verify physical files exist on disk
        p = Path(temp_export_dir)
        assert (p / "build" / "build_report.json").exists()
        assert (p / "security" / "security_gate_report.json").exists()
        assert (p / "infrastructure" / "change_impact_report.json").exists()
        assert (p / "infrastructure" / "drift_report.json").exists()
        assert (p / "performance" / "performance_regression_report.json").exists()
        assert (p / "chaos" / "chaos_pipeline_report.json").exists()
        assert (p / "deployment" / "disposable_env_report.json").exists()
        assert (p / "deployment" / "integration_report.json").exists()
        assert (p / "certification" / "release_decision.json").exists()
        assert (p / "certification" / "production_readiness_certificate.json").exists()
        assert (p / "metadata.json").exists()
        assert (p / "manifest.json").exists()

    # ──────────────────────────────────────────────────────────────────────────
    # 11. Master Runtime Orchestrator Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_runtime_pipeline_execution(self, temp_export_dir):
        runtime = ContinuousVerificationRuntime()
        result = runtime.run_pipeline(export_dir=temp_export_dir)
        assert result["passed"] is True
        assert result["decision"].decision == GateDecision.APPROVED
        assert result["certificate"].certification == "PRODUCTION READY"
        assert result["manifest"].overall_score == 100.0

    @pytest.mark.asyncio
    async def test_runtime_async_run_all(self, temp_export_dir):
        runtime = ContinuousVerificationRuntime()
        manifest = await runtime.run_all(export_dir=temp_export_dir)
        assert manifest.deployment_approved is True
        assert manifest.overall_score == 100.0

    # ──────────────────────────────────────────────────────────────────────────
    # 12. FastAPI Endpoints Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health(self, app_client):
        res = app_client.get("/api/v1/pipeline/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"

    def test_api_stages(self, app_client):
        res = app_client.get("/api/v1/pipeline/stages")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 7

    def test_api_run_pipeline(self, app_client):
        res = app_client.post("/api/v1/pipeline/run")
        assert res.status_code == 200
        data = res.json()
        assert data["deployment_approved"] is True
        assert data["decision"] == "APPROVED"

    def test_api_get_decision(self, app_client):
        res = app_client.get("/api/v1/pipeline/decision")
        assert res.status_code == 200
        data = res.json()
        assert data["decision"] == "APPROVED"

    def test_api_get_certificate(self, app_client):
        res = app_client.get("/api/v1/pipeline/certificate")
        assert res.status_code == 200
        data = res.json()
        assert data["certification"] == "PRODUCTION READY"

    def test_api_get_security_gate(self, app_client):
        res = app_client.get("/api/v1/pipeline/security")
        assert res.status_code == 200
        data = res.json()
        assert data["gate_passed"] is True

    def test_api_get_performance(self, app_client):
        res = app_client.get("/api/v1/pipeline/performance")
        assert res.status_code == 200
        data = res.json()
        assert data["threshold_exceeded"] is False

    def test_api_get_drift(self, app_client):
        res = app_client.get("/api/v1/pipeline/drift")
        assert res.status_code == 200
        data = res.json()
        assert data["drift_detected"] is False

    def test_api_get_manifest(self, app_client):
        res = app_client.get("/api/v1/pipeline/manifest")
        assert res.status_code == 200
        data = res.json()
        assert data["project"] == "DocuTask-Agent"
