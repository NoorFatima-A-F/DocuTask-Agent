"""
Phase 3L: Comprehensive Test Suite for Enterprise Backup, Disaster Recovery & Continuity Framework.
"""

from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_disaster_recovery.domain.models import (
    BackupSecurityReport,
    BusinessImpactAnalysisReport,
    CheckResult,
    CompleteSystemRestoreReport,
    ConfigurationRecoveryReport,
    DatabaseRecoveryReport,
    DisasterRecoveryArchitectureReport,
    DisasterRecoveryTier,
    DRAutomationReport,
    DRFailureSimulationReport,
    PITRReport,
    RecoveryObjectivesReport,
    RecoveryObservabilityReport,
    SecretRecoveryReport,
    StorageRecoveryReport,
    VerificationManifest,
    VerificationStatus,
)
from app.platform_verification.enterprise_disaster_recovery.domain.interfaces import (
    IDisasterRecoveryVerifier,
)
from app.platform_verification.enterprise_disaster_recovery.verifiers import (
    BackupSecurityVerifier,
    BusinessImpactAnalysisVerifier,
    CompleteSystemRestoreVerifier,
    ConfigurationRecoveryVerifier,
    DatabaseRecoveryVerifier,
    DisasterRecoveryArchitectureVerifier,
    DRAutomationPipelineVerifier,
    DRFailureSimulationVerifier,
    PITRRecoveryVerifier,
    RecoveryObjectivesVerifier,
    RecoveryObservabilityVerifier,
    SecretRecoveryVerifier,
    StorageRecoveryVerifier,
)
from app.platform_verification.enterprise_disaster_recovery.scoring.disaster_recovery_scorer import (
    DisasterRecoveryScorer,
)
from app.platform_verification.enterprise_disaster_recovery.exporter.disaster_recovery_exporter import (
    DisasterRecoveryExporter,
)
from app.platform_verification.enterprise_disaster_recovery.runtime.disaster_recovery_runtime import (
    DisasterRecoveryRuntime,
)
from app.platform_verification.enterprise_disaster_recovery.api.disaster_recovery_api import (
    router,
)


class TestEnterpriseDisasterRecoveryVerification:
    """Complete test suite for Phase 3L."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_dr_verification"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Verifiers Individual Tests (3L.1 - 3L.13)
    # ──────────────────────────────────────────────────────────────────────────

    def test_3l_1_architecture_verifier(self):
        verifier = DisasterRecoveryArchitectureVerifier()
        assert verifier.verifier_id == "VERIFY-3L.1-DR-ARCHITECTURE"
        assert verifier.phase_id == "3L.1"
        report = verifier.verify()
        assert isinstance(report, DisasterRecoveryArchitectureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert all(c.passed for c in report.checks)
        assert report.components_identified == 15
        assert report.critical_assets == 12
        assert report.architecture_status == "READY"

    def test_3l_2_bia_verifier(self):
        verifier = BusinessImpactAnalysisVerifier()
        assert verifier.verifier_id == "VERIFY-3L.2-BIA"
        assert verifier.phase_id == "3L.2"
        report = verifier.verify()
        assert isinstance(report, BusinessImpactAnalysisReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.tier_0_mission_critical_count == 3
        assert report.total_services_classified == 10

    def test_3l_3_recovery_objectives_verifier(self):
        verifier = RecoveryObjectivesVerifier()
        assert verifier.verifier_id == "VERIFY-3L.3-RECOVERY-OBJECTIVES"
        assert verifier.phase_id == "3L.3"
        report = verifier.verify()
        assert isinstance(report, RecoveryObjectivesReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.observed_rto_minutes <= 60.0
        assert report.observed_rpo_minutes <= 15.0
        assert report.rto_compliance_pct == 100.0

    def test_3l_4_database_recovery_verifier(self):
        verifier = DatabaseRecoveryVerifier()
        assert verifier.verifier_id == "VERIFY-3L.4-DATABASE-RECOVERY"
        assert verifier.phase_id == "3L.4"
        report = verifier.verify()
        assert isinstance(report, DatabaseRecoveryReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.data_loss_records == 0
        assert report.schema_integrity_verified is True
        assert len(report.tables_validated) == 6

    def test_3l_5_storage_recovery_verifier(self):
        verifier = StorageRecoveryVerifier()
        assert verifier.verifier_id == "VERIFY-3L.5-STORAGE-RECOVERY"
        assert verifier.phase_id == "3L.5"
        report = verifier.verify()
        assert isinstance(report, StorageRecoveryReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.missing_files_count == 0
        assert report.sha256_match_rate_pct == 100.0
        assert report.total_documents_restored == 1500

    def test_3l_6_configuration_recovery_verifier(self):
        verifier = ConfigurationRecoveryVerifier()
        assert verifier.verifier_id == "VERIFY-3L.6-CONFIG-RECOVERY"
        assert verifier.phase_id == "3L.6"
        report = verifier.verify()
        assert isinstance(report, ConfigurationRecoveryReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.config_assets_count == 8
        assert report.environment_templates_restored is True
        assert report.migration_scripts_restored is True

    def test_3l_7_secret_recovery_verifier(self):
        verifier = SecretRecoveryVerifier()
        assert verifier.verifier_id == "VERIFY-3L.7-SECRET-RECOVERY"
        assert verifier.phase_id == "3L.7"
        report = verifier.verify()
        assert isinstance(report, SecretRecoveryReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.total_secrets_protected == 6
        assert report.unauthorized_access_blocked is True
        assert report.zero_plaintext_leakage is True

    def test_3l_8_system_restore_verifier(self):
        verifier = CompleteSystemRestoreVerifier()
        assert verifier.verifier_id == "VERIFY-3L.8-SYSTEM-RESTORE"
        assert verifier.phase_id == "3L.8"
        report = verifier.verify()
        assert isinstance(report, CompleteSystemRestoreReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.user_login_works is True
        assert report.document_upload_works is True
        assert report.ai_processing_works is True
        assert report.total_rebuild_time_minutes <= 60.0

    def test_3l_9_pitr_verifier(self):
        verifier = PITRRecoveryVerifier()
        assert verifier.verifier_id == "VERIFY-3L.9-PITR-RECOVERY"
        assert verifier.phase_id == "3L.9"
        report = verifier.verify()
        assert isinstance(report, PITRReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.pitr_enabled is True
        assert report.wal_archiving_active is True
        assert report.data_loss_records == 0

    def test_3l_10_backup_security_verifier(self):
        verifier = BackupSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3L.10-BACKUP-SECURITY"
        assert verifier.phase_id == "3L.10"
        report = verifier.verify()
        assert isinstance(report, BackupSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.immutable_worm_lock_enabled is True
        assert report.rbac_enforced is True
        assert report.encryption_at_rest == "AES-256"

    def test_3l_11_dr_automation_verifier(self):
        verifier = DRAutomationPipelineVerifier()
        assert verifier.verifier_id == "VERIFY-3L.11-DR-AUTOMATION"
        assert verifier.phase_id == "3L.11"
        report = verifier.verify()
        assert isinstance(report, DRAutomationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.pipeline_fully_automated is True
        assert report.manual_intervention_required is False
        assert report.stages_count == 5

    def test_3l_12_failure_simulation_verifier(self):
        verifier = DRFailureSimulationVerifier()
        assert verifier.verifier_id == "VERIFY-3L.12-FAILURE-SIMULATION"
        assert verifier.phase_id == "3L.12"
        report = verifier.verify()
        assert isinstance(report, DRFailureSimulationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.all_scenarios_recovered is True
        assert report.scenarios_executed == 4
        assert report.infrastructure_loss_recovered is True

    def test_3l_13_recovery_observability_verifier(self):
        verifier = RecoveryObservabilityVerifier()
        assert verifier.verifier_id == "VERIFY-3L.13-RECOVERY-OBSERVABILITY"
        assert verifier.phase_id == "3L.13"
        report = verifier.verify()
        assert isinstance(report, RecoveryObservabilityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.telemetry_pipeline_active is True
        assert report.metrics_captured == 12
        assert report.audit_trail_immutable is True

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Scorer Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_scorer_all_passed(self):
        verifiers = [
            DisasterRecoveryArchitectureVerifier(),
            BusinessImpactAnalysisVerifier(),
            RecoveryObjectivesVerifier(),
            DatabaseRecoveryVerifier(),
            StorageRecoveryVerifier(),
            ConfigurationRecoveryVerifier(),
            SecretRecoveryVerifier(),
            CompleteSystemRestoreVerifier(),
            PITRRecoveryVerifier(),
            BackupSecurityVerifier(),
            DRAutomationPipelineVerifier(),
            DRFailureSimulationVerifier(),
            RecoveryObservabilityVerifier(),
        ]
        reports = [v.verify() for v in verifiers]
        scorer = DisasterRecoveryScorer()
        scorecard = scorer.score(reports, execution_time_seconds=1.45)

        assert scorecard.overall_score == 100.0
        assert scorecard.certification_tier == DisasterRecoveryTier.ENTERPRISE_DR_READY
        assert scorecard.status == VerificationStatus.PASSED
        assert len(scorecard.categories) == 6
        for cat_name, cat in scorecard.categories.items():
            assert cat.score == 100.0

    def test_scorer_partial_failure(self):
        class FailingVerifier(IDisasterRecoveryVerifier):
            @property
            def verifier_id(self) -> str:
                return "VERIFY-3L.1-DR-ARCHITECTURE"

            @property
            def name(self) -> str:
                return "Failing DR Architecture"

            def verify(self):
                return DisasterRecoveryArchitectureReport(
                    verifier_id="VERIFY-3L.1-DR-ARCHITECTURE",
                    phase_id="3L.1",
                    phase_name="Failing Architecture",
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
        scorer = DisasterRecoveryScorer()
        scorecard = scorer.score([failing_report])
        assert scorecard.overall_score < 100.0
        assert scorecard.categories["Backup Reliability"].score == 0.0

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Exporter & Manifest Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_exporter_generates_valid_json_and_sha256(self, temp_export_dir):
        exporter = DisasterRecoveryExporter(export_dir=temp_export_dir)
        verifier = DisasterRecoveryArchitectureVerifier()
        report = verifier.verify()
        written = exporter.export_report(report)
        assert len(written) > 0
        assert (Path(temp_export_dir) / "disaster_recovery_architecture_report.json").exists()

        scorer = DisasterRecoveryScorer()
        scorecard = scorer.score([report])
        scorecard_written = exporter.export_scorecard(scorecard)
        assert len(scorecard_written) > 0
        assert (Path(temp_export_dir) / "disaster_recovery_scorecard.json").exists()

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
        runtime = DisasterRecoveryRuntime()
        result = runtime.run_full_verification(export_dir=temp_export_dir)
        assert result["passed"] is True
        assert result["overall_score"] == 100.0
        assert result["tier"] == DisasterRecoveryTier.ENTERPRISE_DR_READY.value
        assert len(result["reports"]) == 13
        assert runtime.get_latest_scorecard() is not None
        assert runtime.get_latest_manifest() is not None

    def test_runtime_execute_verifier_lookup(self):
        runtime = DisasterRecoveryRuntime()
        report1 = runtime.execute_verifier("3L.1")
        assert report1.phase_id == "3L.1"

        report4 = runtime.execute_verifier("VERIFY-3L.4-DATABASE-RECOVERY")
        assert report4.verifier_id == "VERIFY-3L.4-DATABASE-RECOVERY"

        with pytest.raises(ValueError):
            runtime.execute_verifier("INVALID-ID-999")

    # ──────────────────────────────────────────────────────────────────────────
    # 5. FastAPI REST Endpoints Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health(self, app_client):
        res = app_client.get("/api/v1/disaster-recovery/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"

    def test_api_phases(self, app_client):
        res = app_client.get("/api/v1/disaster-recovery/phases")
        assert res.status_code == 200
        phases = res.json()
        assert len(phases) == 13
        assert phases[0]["phase_id"] == "3L.1"

    def test_api_get_report(self, app_client):
        res = app_client.get("/api/v1/disaster-recovery/reports/3L.1")
        assert res.status_code == 200
        data = res.json()
        assert data["phase_id"] == "3L.1"
        assert data["score"] == 100.0

    def test_api_get_report_not_found(self, app_client):
        res = app_client.get("/api/v1/disaster-recovery/reports/NONEXISTENT")
        assert res.status_code == 404

    def test_api_run_verification(self, app_client):
        res = app_client.post("/api/v1/disaster-recovery/run")
        assert res.status_code == 200
        manifest = res.json()
        assert manifest["overall_score"] == 100.0
        assert manifest["certification_tier"] == "Enterprise Disaster Recovery Ready"
        assert len(manifest["files"]) > 0

    def test_api_scorecard(self, app_client):
        res = app_client.get("/api/v1/disaster-recovery/scorecard")
        assert res.status_code == 200
        scorecard = res.json()
        assert scorecard["overall_score"] == 100.0
        assert scorecard["status"] == "PASSED"

    def test_api_manifest(self, app_client):
        res = app_client.get("/api/v1/disaster-recovery/manifest")
        assert res.status_code == 200
        manifest = res.json()
        assert "files" in manifest
