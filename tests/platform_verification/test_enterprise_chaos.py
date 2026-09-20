"""
Phase 3K: Comprehensive Test Suite for Enterprise Chaos Engineering Verification Framework.
"""

import json
import os
from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_chaos_verification.domain.models import (
    AIProviderFailureReport,
    BaseVerificationReport,
    CascadingFailureReport,
    ChaosObservabilityReport,
    ChaosPipelineReport,
    ChaosReadinessReport,
    ChaosReportGenerationReport,
    ChaosResilienceTier,
    ChaosScorecard,
    CheckResult,
    ContainerFailureReport,
    DatabaseFailureReport,
    NetworkFailureReport,
    QueueFailureReport,
    ResourceExhaustionReport,
    VerificationManifest,
    VerificationStatus,
    WorkerAgentFailureReport,
)
from app.platform_verification.enterprise_chaos_verification.domain.interfaces import (
    IChaosVerifier,
)
from app.platform_verification.enterprise_chaos_verification.verifiers import (
    AIProviderFailureVerifier,
    CascadingFailureVerifier,
    ChaosAutomationPipelineVerifier,
    ChaosObservabilityVerifier,
    ChaosReadinessVerifier,
    ChaosReportGenerationVerifier,
    ContainerFailureVerifier,
    DatabaseFailureVerifier,
    NetworkFailureVerifier,
    QueueFailureVerifier,
    ResourceExhaustionVerifier,
    WorkerAgentFailureVerifier,
)
from app.platform_verification.enterprise_chaos_verification.scoring.chaos_scorer import (
    ChaosScorer,
)
from app.platform_verification.enterprise_chaos_verification.exporter.chaos_exporter import (
    ChaosExporter,
)
from app.platform_verification.enterprise_chaos_verification.runtime.chaos_runtime import (
    ChaosRuntime,
)
from app.platform_verification.enterprise_chaos_verification.api.chaos_api import (
    router,
)


class TestEnterpriseChaosVerification:
    """Complete test suite for Phase 3K."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_chaos_verification"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Verifiers Individual Tests (3K.1 - 3K.12)
    # ──────────────────────────────────────────────────────────────────────────

    def test_3k_1_readiness_verifier(self):
        verifier = ChaosReadinessVerifier()
        assert verifier.verifier_id == "VERIFY-3K.1-CHAOS-READINESS"
        assert verifier.phase_id == "3K.1"
        report = verifier.verify()
        assert isinstance(report, ChaosReadinessReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert all(c.passed for c in report.checks)
        assert report.preflight_passed is True
        assert report.monitoring == "available"
        assert report.rollback == "available"
        assert len(report.preflight_items) == 4

    def test_3k_2_container_failure_verifier(self):
        verifier = ContainerFailureVerifier()
        assert verifier.verifier_id == "VERIFY-3K.2-CONTAINER-FAILURE"
        assert verifier.phase_id == "3K.2"
        report = verifier.verify()
        assert isinstance(report, ContainerFailureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.experiments_executed == 2
        assert report.total_data_loss_events == 0
        assert len(report.scenarios) == 2

    def test_3k_3_database_failure_verifier(self):
        verifier = DatabaseFailureVerifier()
        assert verifier.verifier_id == "VERIFY-3K.3-DATABASE-FAILURE"
        assert verifier.phase_id == "3K.3"
        report = verifier.verify()
        assert isinstance(report, DatabaseFailureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.lost_records_count == 0
        assert report.zero_corruption_verified is True
        assert len(report.state_transitions) == 3

    def test_3k_4_queue_failure_verifier(self):
        verifier = QueueFailureVerifier()
        assert verifier.verifier_id == "VERIFY-3K.4-QUEUE-FAILURE"
        assert verifier.phase_id == "3K.4"
        report = verifier.verify()
        assert isinstance(report, QueueFailureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.messages_lost_count == 0
        assert report.degraded_mode_activated is True
        assert report.idempotency_enforced is True

    def test_3k_5_network_failure_verifier(self):
        verifier = NetworkFailureVerifier()
        assert verifier.verifier_id == "VERIFY-3K.5-NETWORK-FAILURE"
        assert verifier.phase_id == "3K.5"
        report = verifier.verify()
        assert isinstance(report, NetworkFailureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.circuit_breaker_verified is True
        assert report.dependency_isolation_verified is True
        assert len(report.tests) == 3

    def test_3k_6_ai_provider_failure_verifier(self):
        verifier = AIProviderFailureVerifier()
        assert verifier.verifier_id == "VERIFY-3K.6-AI-PROVIDER-FAILURE"
        assert verifier.phase_id == "3K.6"
        report = verifier.verify()
        assert isinstance(report, AIProviderFailureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.gemini_outage_simulated is True
        assert report.document_loss_count == 0
        assert len(report.scenarios) == 2

    def test_3k_7_resource_exhaustion_verifier(self):
        verifier = ResourceExhaustionVerifier()
        assert verifier.verifier_id == "VERIFY-3K.7-RESOURCE-EXHAUSTION"
        assert verifier.phase_id == "3K.7"
        report = verifier.verify()
        assert isinstance(report, ResourceExhaustionReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.disk_full_rejection_verified is True
        assert report.zero_unhandled_crashes is True
        assert len(report.scenarios) == 3

    def test_3k_8_worker_agent_failure_verifier(self):
        verifier = WorkerAgentFailureVerifier()
        assert verifier.verifier_id == "VERIFY-3K.8-WORKER-AGENT-FAILURE"
        assert verifier.phase_id == "3K.8"
        report = verifier.verify()
        assert isinstance(report, WorkerAgentFailureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.infinite_loop_mitigated is True
        assert report.duplicate_worker_idempotency_verified is True
        assert len(report.scenarios) == 2

    def test_3k_9_cascading_failure_verifier(self):
        verifier = CascadingFailureVerifier()
        assert verifier.verifier_id == "VERIFY-3K.9-CASCADING-FAILURE"
        assert verifier.phase_id == "3K.9"
        report = verifier.verify()
        assert isinstance(report, CascadingFailureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.collapse_prevented is True
        assert report.blast_radius_isolated is True
        assert len(report.containment_stages) == 4

    def test_3k_10_chaos_pipeline_verifier(self):
        verifier = ChaosAutomationPipelineVerifier()
        assert verifier.verifier_id == "VERIFY-3K.10-CHAOS-AUTOMATION-PIPELINE"
        assert verifier.phase_id == "3K.10"
        report = verifier.verify()
        assert isinstance(report, ChaosPipelineReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.pipeline_automated is True
        assert report.ci_cd_integration_ready is True
        assert report.stages_count == 8

    def test_3k_11_observability_verifier(self):
        verifier = ChaosObservabilityVerifier()
        assert verifier.verifier_id == "VERIFY-3K.11-CHAOS-OBSERVABILITY"
        assert verifier.phase_id == "3K.11"
        report = verifier.verify()
        assert isinstance(report, ChaosObservabilityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.metrics_captured is True
        assert report.traces_reconstructed is True
        assert report.e2e_forensic_trace_verified is True

    def test_3k_12_reporting_verifier(self):
        verifier = ChaosReportGenerationVerifier()
        assert verifier.verifier_id == "VERIFY-3K.12-CHAOS-REPORTING"
        assert verifier.phase_id == "3K.12"
        report = verifier.verify()
        assert isinstance(report, ChaosReportGenerationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.total_experiments_documented == 8
        assert report.all_experiments_passed is True
        assert len(report.experiments_summary) == 8

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Scorer Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_scorer_all_passed(self):
        verifiers = [
            ChaosReadinessVerifier(),
            ContainerFailureVerifier(),
            DatabaseFailureVerifier(),
            QueueFailureVerifier(),
            NetworkFailureVerifier(),
            AIProviderFailureVerifier(),
            ResourceExhaustionVerifier(),
            WorkerAgentFailureVerifier(),
            CascadingFailureVerifier(),
            ChaosAutomationPipelineVerifier(),
            ChaosObservabilityVerifier(),
            ChaosReportGenerationVerifier(),
        ]
        reports = [v.verify() for v in verifiers]
        scorer = ChaosScorer()
        scorecard = scorer.score(reports, execution_time_seconds=1.25)

        assert scorecard.overall_score == 100.0
        assert scorecard.certification_tier == ChaosResilienceTier.CHAOS_RESILIENT
        assert scorecard.status == VerificationStatus.PASSED
        assert len(scorecard.categories) == 6
        for cat_name, cat in scorecard.categories.items():
            assert cat.score == 100.0

    def test_scorer_partial_failure(self):
        class FailingVerifier(IChaosVerifier):
            @property
            def verifier_id(self) -> str:
                return "VERIFY-3K.1-CHAOS-READINESS"

            @property
            def name(self) -> str:
                return "Failing Readiness"

            def verify(self):
                return ChaosReadinessReport(
                    verifier_id="VERIFY-3K.1-CHAOS-READINESS",
                    phase_id="3K.1",
                    phase_name="Failing Readiness",
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
        scorer = ChaosScorer()
        scorecard = scorer.score([failing_report])
        assert scorecard.overall_score < 100.0
        assert scorecard.categories["Failure Detection"].score == 0.0

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Exporter & Manifest Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_exporter_generates_valid_json_and_sha256(self, temp_export_dir):
        exporter = ChaosExporter(export_dir=temp_export_dir)
        verifier = ChaosReadinessVerifier()
        report = verifier.verify()
        written = exporter.export_report(report)
        assert len(written) > 0
        assert (Path(temp_export_dir) / "chaos_readiness_report.json").exists()

        scorer = ChaosScorer()
        scorecard = scorer.score([report])
        scorecard_written = exporter.export_scorecard(scorecard)
        assert len(scorecard_written) > 0
        assert (Path(temp_export_dir) / "resilience_score.json").exists()

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
        runtime = ChaosRuntime()
        result = runtime.run_full_verification(export_dir=temp_export_dir)
        assert result["passed"] is True
        assert result["overall_score"] == 100.0
        assert result["tier"] == ChaosResilienceTier.CHAOS_RESILIENT.value
        assert len(result["reports"]) == 12
        assert runtime.get_latest_scorecard() is not None
        assert runtime.get_latest_manifest() is not None

    def test_runtime_execute_verifier_lookup(self):
        runtime = ChaosRuntime()
        report1 = runtime.execute_verifier("3K.1")
        assert report1.phase_id == "3K.1"

        report6 = runtime.execute_verifier("VERIFY-3K.6-AI-PROVIDER-FAILURE")
        assert report6.verifier_id == "VERIFY-3K.6-AI-PROVIDER-FAILURE"

        with pytest.raises(ValueError):
            runtime.execute_verifier("INVALID-ID-999")

    # ──────────────────────────────────────────────────────────────────────────
    # 5. FastAPI REST Endpoints Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health(self, app_client):
        res = app_client.get("/api/v1/chaos/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"

    def test_api_phases(self, app_client):
        res = app_client.get("/api/v1/chaos/phases")
        assert res.status_code == 200
        phases = res.json()
        assert len(phases) == 12
        assert phases[0]["phase_id"] == "3K.1"

    def test_api_get_report(self, app_client):
        res = app_client.get("/api/v1/chaos/reports/3K.1")
        assert res.status_code == 200
        data = res.json()
        assert data["phase_id"] == "3K.1"
        assert data["score"] == 100.0

    def test_api_get_report_not_found(self, app_client):
        res = app_client.get("/api/v1/chaos/reports/NONEXISTENT")
        assert res.status_code == 404

    def test_api_run_verification(self, app_client):
        res = app_client.post("/api/v1/chaos/run")
        assert res.status_code == 200
        manifest = res.json()
        assert manifest["overall_score"] == 100.0
        assert manifest["certification_tier"] == "Chaos Resilient"
        assert len(manifest["files"]) > 0

    def test_api_scorecard(self, app_client):
        res = app_client.get("/api/v1/chaos/scorecard")
        assert res.status_code == 200
        scorecard = res.json()
        assert scorecard["overall_score"] == 100.0
        assert scorecard["status"] == "PASSED"

    def test_api_manifest(self, app_client):
        res = app_client.get("/api/v1/chaos/manifest")
        assert res.status_code == 200
        manifest = res.json()
        assert "files" in manifest
