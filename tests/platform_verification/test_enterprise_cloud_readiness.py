"""
Phase 3M: Comprehensive Test Suite for Enterprise Cloud Readiness Verification Framework.
"""

from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_cloud_readiness.domain.models import (
    AutoScalingReport,
    CheckResult,
    CloudArchitectureAssessmentReport,
    CloudComputeResourceReport,
    CloudMigrationSimulationReport,
    CloudNetworkingReport,
    CloudObservabilityReport,
    CloudQueueWorkerReport,
    CloudReadinessTier,
    CloudSecretReport,
    CloudSecurityReport,
    CloudStorageReport,
    ContainerCloudCompatibilityReport,
    IaCVerificationReport,
    KubernetesReadinessReport,
    ManagedDatabaseReport,
    MultiCloudPortabilityReport,
    VerificationManifest,
    VerificationStatus,
)
from app.platform_verification.enterprise_cloud_readiness.domain.interfaces import (
    ICloudReadinessVerifier,
)
from app.platform_verification.enterprise_cloud_readiness.verifiers import (
    AutoScalingReadinessVerifier,
    CloudArchitectureAssessmentVerifier,
    CloudComputeResourceVerifier,
    CloudMigrationSimulationVerifier,
    CloudNetworkingVerifier,
    CloudObservabilityCompatibilityVerifier,
    CloudQueueWorkerScalabilityVerifier,
    CloudSecretManagementVerifier,
    CloudSecurityVerifier,
    CloudStorageCompatibilityVerifier,
    ContainerCloudCompatibilityVerifier,
    InfrastructureAsCodeVerifier,
    KubernetesReadinessVerifier,
    ManagedDatabaseReadinessVerifier,
    MultiCloudPortabilityVerifier,
)
from app.platform_verification.enterprise_cloud_readiness.scoring.cloud_readiness_scorer import (
    CloudReadinessScorer,
)
from app.platform_verification.enterprise_cloud_readiness.exporter.cloud_readiness_exporter import (
    CloudReadinessExporter,
)
from app.platform_verification.enterprise_cloud_readiness.runtime.cloud_readiness_runtime import (
    CloudReadinessRuntime,
)
from app.platform_verification.enterprise_cloud_readiness.api.cloud_readiness_api import (
    router,
)


class TestEnterpriseCloudReadinessVerification:
    """Complete test suite for Phase 3M."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_cloud_readiness"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Verifiers Individual Tests (3M.1 - 3M.15)
    # ──────────────────────────────────────────────────────────────────────────

    def test_3m_1_architecture_verifier(self):
        verifier = CloudArchitectureAssessmentVerifier()
        assert verifier.verifier_id == "VERIFY-3M.1-CLOUD-ARCH"
        assert verifier.phase_id == "3M.1"
        report = verifier.verify()
        assert isinstance(report, CloudArchitectureAssessmentReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert all(c.passed for c in report.checks)
        assert report.layers_evaluated == 7
        assert report.migration_status == "READY"

    def test_3m_2_container_compatibility_verifier(self):
        verifier = ContainerCloudCompatibilityVerifier()
        assert verifier.verifier_id == "VERIFY-3M.2-CONTAINER-CLOUD"
        assert verifier.phase_id == "3M.2"
        report = verifier.verify()
        assert isinstance(report, ContainerCloudCompatibilityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.runtimes_tested == 7
        assert report.statelessness_verified is True
        assert report.graceful_sigterm_handling is True

    def test_3m_3_compute_resource_verifier(self):
        verifier = CloudComputeResourceVerifier()
        assert verifier.verifier_id == "VERIFY-3M.3-COMPUTE-RESOURCE"
        assert verifier.phase_id == "3M.3"
        report = verifier.verify()
        assert isinstance(report, CloudComputeResourceReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.services_profiled == 3
        assert report.oom_prevention_verified is True
        assert report.cpu_throttling_prevented is True

    def test_3m_4_networking_verifier(self):
        verifier = CloudNetworkingVerifier()
        assert verifier.verifier_id == "VERIFY-3M.4-CLOUD-NETWORKING"
        assert verifier.phase_id == "3M.4"
        report = verifier.verify()
        assert isinstance(report, CloudNetworkingReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.public_endpoints_restricted_to_ingress is True
        assert report.database_isolated_in_private_subnet is True
        assert report.redis_isolated_in_private_subnet is True

    def test_3m_5_storage_verifier(self):
        verifier = CloudStorageCompatibilityVerifier()
        assert verifier.verifier_id == "VERIFY-3M.5-CLOUD-STORAGE"
        assert verifier.phase_id == "3M.5"
        report = verifier.verify()
        assert isinstance(report, CloudStorageReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.local_uploads_path_dependency_removed is True
        assert report.s3_compatible is True
        assert report.gcs_compatible is True
        assert report.azure_blob_compatible is True

    def test_3m_6_managed_db_verifier(self):
        verifier = ManagedDatabaseReadinessVerifier()
        assert verifier.verifier_id == "VERIFY-3M.6-MANAGED-DB"
        assert verifier.phase_id == "3M.6"
        report = verifier.verify()
        assert isinstance(report, ManagedDatabaseReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.no_localhost_assumptions is True
        assert report.ssl_encryption_enforced is True
        assert report.automatic_reconnection_verified is True

    def test_3m_7_queue_worker_verifier(self):
        verifier = CloudQueueWorkerScalabilityVerifier()
        assert verifier.verifier_id == "VERIFY-3M.7-WORKER-SCALING"
        assert verifier.phase_id == "3M.7"
        report = verifier.verify()
        assert isinstance(report, CloudQueueWorkerReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.burst_load_10k_handled is True
        assert report.duplicate_task_prevention_rate_pct == 100.0
        assert report.dlq_isolation_verified is True

    def test_3m_8_autoscaling_verifier(self):
        verifier = AutoScalingReadinessVerifier()
        assert verifier.verifier_id == "VERIFY-3M.8-AUTOSCALING"
        assert verifier.phase_id == "3M.8"
        report = verifier.verify()
        assert isinstance(report, AutoScalingReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.horizontal_pod_autoscaler_ready is True
        assert report.scale_out_speed_seconds <= 30.0
        assert len(report.dimensions) == 3

    def test_3m_9_cloud_secret_verifier(self):
        verifier = CloudSecretManagementVerifier()
        assert verifier.verifier_id == "VERIFY-3M.9-CLOUD-SECRETS"
        assert verifier.phase_id == "3M.9"
        report = verifier.verify()
        assert isinstance(report, CloudSecretReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.env_file_decoupled is True
        assert report.aws_secrets_manager_supported is True
        assert report.gcp_secret_manager_supported is True
        assert report.azure_key_vault_supported is True

    def test_3m_10_cloud_observability_verifier(self):
        verifier = CloudObservabilityCompatibilityVerifier()
        assert verifier.verifier_id == "VERIFY-3M.10-CLOUD-OBSERVABILITY"
        assert verifier.phase_id == "3M.10"
        report = verifier.verify()
        assert isinstance(report, CloudObservabilityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.opentelemetry_standardized is True
        assert report.structured_json_logging is True
        assert len(report.sinks) == 4

    def test_3m_11_iac_verifier(self):
        verifier = InfrastructureAsCodeVerifier()
        assert verifier.verifier_id == "VERIFY-3M.11-IAC"
        assert verifier.phase_id == "3M.11"
        report = verifier.verify()
        assert isinstance(report, IaCVerificationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.terraform_modules_verified is True
        assert report.kubernetes_helm_charts_verified is True
        assert report.total_resources_managed == 28

    def test_3m_12_kubernetes_verifier(self):
        verifier = KubernetesReadinessVerifier()
        assert verifier.verifier_id == "VERIFY-3M.12-KUBERNETES-READINESS"
        assert verifier.phase_id == "3M.12"
        report = verifier.verify()
        assert isinstance(report, KubernetesReadinessReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.deployments_ready is True
        assert report.readiness_liveness_probes_active is True
        assert len(report.manifests) == 8

    def test_3m_13_cloud_security_verifier(self):
        verifier = CloudSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3M.13-CLOUD-SECURITY"
        assert verifier.phase_id == "3M.13"
        report = verifier.verify()
        assert isinstance(report, CloudSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.least_privilege_iam_enforced is True
        assert report.non_root_container_execution is True
        assert report.vulnerability_scanning_clean is True

    def test_3m_14_portability_verifier(self):
        verifier = MultiCloudPortabilityVerifier()
        assert verifier.verifier_id == "VERIFY-3M.14-MULTI-CLOUD"
        assert verifier.phase_id == "3M.14"
        report = verifier.verify()
        assert isinstance(report, MultiCloudPortabilityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.zero_code_change_migration is True
        assert report.vendor_lockin_risk == "ZERO"
        assert len(report.parity_benchmarks) == 4

    def test_3m_15_migration_simulation_verifier(self):
        verifier = CloudMigrationSimulationVerifier()
        assert verifier.verifier_id == "VERIFY-3M.15-MIGRATION-SIM"
        assert verifier.phase_id == "3M.15"
        report = verifier.verify()
        assert isinstance(report, CloudMigrationSimulationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.simulation_successful is True
        assert report.steps_passed == 8
        assert report.total_migration_time_minutes <= 15.0

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Scorer Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_scorer_all_passed(self):
        verifiers = [
            CloudArchitectureAssessmentVerifier(),
            ContainerCloudCompatibilityVerifier(),
            CloudComputeResourceVerifier(),
            CloudNetworkingVerifier(),
            CloudStorageCompatibilityVerifier(),
            ManagedDatabaseReadinessVerifier(),
            CloudQueueWorkerScalabilityVerifier(),
            AutoScalingReadinessVerifier(),
            CloudSecretManagementVerifier(),
            CloudObservabilityCompatibilityVerifier(),
            InfrastructureAsCodeVerifier(),
            KubernetesReadinessVerifier(),
            CloudSecurityVerifier(),
            MultiCloudPortabilityVerifier(),
            CloudMigrationSimulationVerifier(),
        ]
        reports = [v.verify() for v in verifiers]
        scorer = CloudReadinessScorer()
        scorecard = scorer.score(reports, execution_time_seconds=1.75)

        assert scorecard.overall_score == 100.0
        assert scorecard.certification_tier == CloudReadinessTier.CLOUD_NATIVE_READY
        assert scorecard.status == VerificationStatus.PASSED
        assert len(scorecard.categories) == 7
        for cat_name, cat in scorecard.categories.items():
            assert cat.score == 100.0

    def test_scorer_partial_failure(self):
        class FailingVerifier(ICloudReadinessVerifier):
            @property
            def verifier_id(self) -> str:
                return "VERIFY-3M.1-CLOUD-ARCH"

            @property
            def name(self) -> str:
                return "Failing Cloud Architecture"

            def verify(self):
                return CloudArchitectureAssessmentReport(
                    verifier_id="VERIFY-3M.1-CLOUD-ARCH",
                    phase_id="3M.1",
                    phase_name="Failing Cloud Architecture",
                    status=VerificationStatus.FAILED,
                    score=0.0,
                    checks=[
                        CheckResult(name="Check 1", passed=False, details="Failed", metrics={}),
                        CheckResult(name="Check 2", passed=False, details="Failed", metrics={}),
                        CheckResult(name="Check 3", passed=False, details="Failed", metrics={}),
                        CheckResult(name="Check 4", passed=False, details="Failed", metrics={}),
                    ],
                )

        failing_report = FailingVerifier().verify()
        scorer = CloudReadinessScorer()
        scorecard = scorer.score([failing_report])
        assert scorecard.overall_score < 100.0
        assert scorecard.categories["Container Compatibility"].score == 0.0

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Exporter & Manifest Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_exporter_generates_valid_json_and_sha256(self, temp_export_dir):
        exporter = CloudReadinessExporter(export_dir=temp_export_dir)
        verifier = CloudArchitectureAssessmentVerifier()
        report = verifier.verify()
        written = exporter.export_report(report)
        assert len(written) > 0
        assert (Path(temp_export_dir) / "cloud_architecture_assessment.json").exists()

        scorer = CloudReadinessScorer()
        scorecard = scorer.score([report])
        scorecard_written = exporter.export_scorecard(scorecard)
        assert len(scorecard_written) > 0
        assert (Path(temp_export_dir) / "cloud_readiness_scorecard.json").exists()

        manifest = exporter.generate_manifest(scorecard, [report])
        assert isinstance(manifest, VerificationManifest)
        assert len(manifest.files) >= 2
        assert (Path(temp_export_dir) / "metadata.json").exists()
        assert (Path(temp_export_dir) / "manifest.json").exists()

        # Check sha256
        for fentry in manifest.files:
            assert len(fentry.sha256) == 64
            assert fentry.size_bytes > 0

    # ──────────────────────────────────────────────────────────────────────────
    # 4. Runtime Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_runtime_run_full_verification(self, temp_export_dir):
        runtime = CloudReadinessRuntime()
        result = runtime.run_full_verification(export_dir=temp_export_dir)
        assert result["passed"] is True
        assert result["overall_score"] == 100.0
        assert result["tier"] == CloudReadinessTier.CLOUD_NATIVE_READY.value
        assert len(result["reports"]) == 15
        assert runtime.get_latest_scorecard() is not None
        assert runtime.get_latest_manifest() is not None

    def test_runtime_execute_verifier_lookup(self):
        runtime = CloudReadinessRuntime()
        report1 = runtime.execute_verifier("3M.1")
        assert report1.phase_id == "3M.1"

        report6 = runtime.execute_verifier("VERIFY-3M.6-MANAGED-DB")
        assert report6.verifier_id == "VERIFY-3M.6-MANAGED-DB"

        with pytest.raises(ValueError):
            runtime.execute_verifier("INVALID-ID-999")

    # ──────────────────────────────────────────────────────────────────────────
    # 5. FastAPI REST Endpoints Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health(self, app_client):
        res = app_client.get("/api/v1/cloud-readiness/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"

    def test_api_phases(self, app_client):
        res = app_client.get("/api/v1/cloud-readiness/phases")
        assert res.status_code == 200
        phases = res.json()
        assert len(phases) == 15
        assert phases[0]["phase_id"] == "3M.1"

    def test_api_get_report(self, app_client):
        res = app_client.get("/api/v1/cloud-readiness/reports/3M.1")
        assert res.status_code == 200
        data = res.json()
        assert data["phase_id"] == "3M.1"
        assert data["score"] == 100.0

    def test_api_get_report_not_found(self, app_client):
        res = app_client.get("/api/v1/cloud-readiness/reports/NONEXISTENT")
        assert res.status_code == 404

    def test_api_run_verification(self, app_client):
        res = app_client.post("/api/v1/cloud-readiness/run")
        assert res.status_code == 200
        manifest = res.json()
        assert manifest["overall_score"] == 100.0
        assert manifest["certification_tier"] == "Cloud Native Ready"
        assert len(manifest["files"]) > 0

    def test_api_scorecard(self, app_client):
        res = app_client.get("/api/v1/cloud-readiness/scorecard")
        assert res.status_code == 200
        scorecard = res.json()
        assert scorecard["overall_score"] == 100.0
        assert scorecard["status"] == "PASSED"

    def test_api_manifest(self, app_client):
        res = app_client.get("/api/v1/cloud-readiness/manifest")
        assert res.status_code == 200
        manifest = res.json()
        assert "files" in manifest
