"""
Phase 3N: Comprehensive Test Suite for Enterprise Infrastructure Security Verification Framework.
"""

import json
import os
from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_infrastructure_security.domain.models import (
    AISecurityReport,
    APISecurityReport,
    BaseVerificationReport,
    CheckResult,
    CICDSecurityReport,
    ContainerSecurityReport,
    DatabaseSecurityReport,
    IAMSecurityReport,
    ImageSupplyChainReport,
    NetworkSecurityReport,
    SecretSecurityReport,
    SecurityArchitectureReport,
    SecurityAttackSimulationReport,
    SecurityCertificationTier,
    SecurityMonitoringReport,
    SecurityScorecard,
    ServiceSecurityReport,
    StorageSecurityReport,
    ThreatModelReport,
    VerificationManifest,
    VerificationStatus,
    VulnerabilityReport,
)
from app.platform_verification.enterprise_infrastructure_security.domain.interfaces import (
    IInfrastructureSecurityVerifier,
)
from app.platform_verification.enterprise_infrastructure_security.verifiers import (
    AIInfrastructureSecurityVerifier,
    APIInfrastructureSecurityVerifier,
    CICDSecurityGateVerifier,
    ContainerSecurityVerifier,
    DatabaseSecurityVerifier,
    IAMSecurityVerifier,
    ImageSupplyChainSecurityVerifier,
    NetworkSecurityVerifier,
    SecretSecurityVerifier,
    SecurityArchitectureVerifier,
    SecurityFailureSimulationVerifier,
    SecurityObservabilityVerifier,
    ServiceToServiceSecurityVerifier,
    StorageSecurityVerifier,
    ThreatModelingVerifier,
    VulnerabilityManagementVerifier,
)
from app.platform_verification.enterprise_infrastructure_security.scoring.infrastructure_security_scorer import (
    InfrastructureSecurityScorer,
)
from app.platform_verification.enterprise_infrastructure_security.exporter.infrastructure_security_exporter import (
    InfrastructureSecurityExporter,
)
from app.platform_verification.enterprise_infrastructure_security.runtime.infrastructure_security_runtime import (
    InfrastructureSecurityRuntime,
)
from app.platform_verification.enterprise_infrastructure_security.api.infrastructure_security_api import (
    router,
)


class TestEnterpriseInfrastructureSecurityVerification:
    """Complete test suite for Phase 3N."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_security_verification"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Verifiers Individual Tests (3N.1 - 3N.16)
    # ──────────────────────────────────────────────────────────────────────────

    def test_3n_1_architecture_verifier(self):
        verifier = SecurityArchitectureVerifier()
        assert verifier.verifier_id == "VERIFY-3N.1-SEC-ARCH"
        assert verifier.phase_id == "3N.1"
        report = verifier.verify()
        assert isinstance(report, SecurityArchitectureReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert all(c.passed for c in report.checks)
        assert report.assets_identified == 25
        assert report.attack_surface == "Minimal / Well-Segmented"
        assert report.trust_boundaries_count == 5

    def test_3n_2_threat_modeling_verifier(self):
        verifier = ThreatModelingVerifier()
        assert verifier.verifier_id == "VERIFY-3N.2-THREAT-MODEL"
        assert verifier.phase_id == "3N.2"
        report = verifier.verify()
        assert isinstance(report, ThreatModelReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.threats_analyzed == 6
        assert report.unmitigated_threats == 0
        assert len(report.stride_categories) == 6

    def test_3n_3_container_security_verifier(self):
        verifier = ContainerSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.3-CONTAINER-SEC"
        assert verifier.phase_id == "3N.3"
        report = verifier.verify()
        assert isinstance(report, ContainerSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.containers_audited == 4
        assert report.non_root_execution_verified is True
        assert report.read_only_rootfs_verified is True
        assert report.privilege_escalation_prevented is True

    def test_3n_4_supply_chain_verifier(self):
        verifier = ImageSupplyChainSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.4-SUPPLY-CHAIN"
        assert verifier.phase_id == "3N.4"
        report = verifier.verify()
        assert isinstance(report, ImageSupplyChainReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.sbom_generated is True
        assert report.image_signing_verified is True
        assert report.provenance_attestation_present is True
        assert len(report.artifacts) == 3

    def test_3n_5_vulnerability_verifier(self):
        verifier = VulnerabilityManagementVerifier()
        assert verifier.verifier_id == "VERIFY-3N.5-VULN-MGMT"
        assert verifier.phase_id == "3N.5"
        report = verifier.verify()
        assert isinstance(report, VulnerabilityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.critical_vulnerabilities_count == 0
        assert report.high_vulnerabilities_count == 0
        assert report.zero_critical_policy_met is True
        assert len(report.scans) == 3

    def test_3n_6_secret_verifier(self):
        verifier = SecretSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.6-SECRET-SEC"
        assert verifier.phase_id == "3N.6"
        report = verifier.verify()
        assert isinstance(report, SecretSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.git_history_clean is True
        assert report.docker_image_clean is True
        assert report.logs_sanitized is True
        assert report.secret_rotation_verified is True
        assert len(report.targets) == 4

    def test_3n_7_iam_verifier(self):
        verifier = IAMSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.7-IAM-SEC"
        assert verifier.phase_id == "3N.7"
        report = verifier.verify()
        assert isinstance(report, IAMSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.rbac_enforced is True
        assert report.least_privilege_verified is True
        assert report.privilege_escalation_blocked is True
        assert len(report.roles_audited) == 4

    def test_3n_8_network_verifier(self):
        verifier = NetworkSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.8-NETWORK-SEC"
        assert verifier.phase_id == "3N.8"
        report = verifier.verify()
        assert isinstance(report, NetworkSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.public_network_segregated is True
        assert report.database_port_isolated is True
        assert report.redis_port_isolated is True
        assert report.firewall_rules_enforced is True
        assert len(report.rules) == 4

    def test_3n_9_service_verifier(self):
        verifier = ServiceToServiceSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.9-SERVICE-SEC"
        assert verifier.phase_id == "3N.9"
        report = verifier.verify()
        assert isinstance(report, ServiceSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.internal_authentication_enforced is True
        assert report.mtls_readiness_verified is True
        assert report.unauthorized_service_rejection is True
        assert len(report.channels) == 4

    def test_3n_10_api_infrastructure_verifier(self):
        verifier = APIInfrastructureSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.10-API-SEC"
        assert verifier.phase_id == "3N.10"
        report = verifier.verify()
        assert isinstance(report, APISecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.jwt_auth_enforced is True
        assert report.rate_limiting_active is True
        assert report.input_validation_strict is True
        assert report.sql_injection_blocked is True
        assert report.xss_injection_blocked is True
        assert len(report.defenses) == 6

    def test_3n_11_database_security_verifier(self):
        verifier = DatabaseSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.11-DATABASE-SEC"
        assert verifier.phase_id == "3N.11"
        report = verifier.verify()
        assert isinstance(report, DatabaseSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.ssl_connections_enforced is True
        assert report.least_privilege_user_enforced is True
        assert report.ddl_destruction_blocked is True
        assert report.audit_logging_active is True
        assert len(report.pillars) == 4

    def test_3n_12_storage_security_verifier(self):
        verifier = StorageSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.12-STORAGE-SEC"
        assert verifier.phase_id == "3N.12"
        report = verifier.verify()
        assert isinstance(report, StorageSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.encryption_at_rest_verified is True
        assert report.cross_tenant_access_blocked is True
        assert report.signed_urls_active is True
        assert report.audit_access_logs_enabled is True
        assert len(report.buckets) == 4

    def test_3n_13_ai_security_verifier(self):
        verifier = AIInfrastructureSecurityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.13-AI-SEC"
        assert verifier.phase_id == "3N.13"
        report = verifier.verify()
        assert isinstance(report, AISecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.prompt_injection_neutralized is True
        assert report.ai_secret_leakage_prevented is True
        assert report.output_schema_sanitized is True
        assert report.malicious_document_mitigated is True
        assert len(report.defenses) == 4

    def test_3n_14_cicd_security_verifier(self):
        verifier = CICDSecurityGateVerifier()
        assert verifier.verifier_id == "VERIFY-3N.14-CICD-SEC"
        assert verifier.phase_id == "3N.14"
        report = verifier.verify()
        assert isinstance(report, CICDSecurityReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.secret_scan_gate_active is True
        assert report.dependency_scan_gate_active is True
        assert report.image_scan_gate_active is True
        assert report.insecure_deployments_blocked is True
        assert len(report.gates) == 6

    def test_3n_15_attack_sim_verifier(self):
        verifier = SecurityFailureSimulationVerifier()
        assert verifier.verifier_id == "VERIFY-3N.15-ATTACK-SIM"
        assert verifier.phase_id == "3N.15"
        report = verifier.verify()
        assert isinstance(report, SecurityAttackSimulationReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.scenarios_executed == 5
        assert report.all_attacks_neutralized is True
        assert report.credential_leak_detected_and_rotated is True
        assert report.unauthorized_db_access_blocked is True
        assert report.container_escape_prevented is True
        assert len(report.scenarios) == 5

    def test_3n_16_monitoring_verifier(self):
        verifier = SecurityObservabilityVerifier()
        assert verifier.verifier_id == "VERIFY-3N.16-SEC-MONITORING"
        assert verifier.phase_id == "3N.16"
        report = verifier.verify()
        assert isinstance(report, SecurityMonitoringReport)
        assert report.status == VerificationStatus.PASSED
        assert report.score == 100.0
        assert len(report.checks) == 4
        assert report.siem_integration_active is True
        assert report.auth_failure_alerts_active is True
        assert report.anomaly_detection_active is True
        assert report.immutable_audit_logs is True
        assert len(report.events) == 5

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Scorer Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_scorer_all_passed(self):
        verifiers = [
            SecurityArchitectureVerifier(),
            ThreatModelingVerifier(),
            ContainerSecurityVerifier(),
            ImageSupplyChainSecurityVerifier(),
            VulnerabilityManagementVerifier(),
            SecretSecurityVerifier(),
            IAMSecurityVerifier(),
            NetworkSecurityVerifier(),
            ServiceToServiceSecurityVerifier(),
            APIInfrastructureSecurityVerifier(),
            DatabaseSecurityVerifier(),
            StorageSecurityVerifier(),
            AIInfrastructureSecurityVerifier(),
            CICDSecurityGateVerifier(),
            SecurityFailureSimulationVerifier(),
            SecurityObservabilityVerifier(),
        ]
        reports = [v.verify() for v in verifiers]
        scorer = InfrastructureSecurityScorer()
        scorecard = scorer.score(reports, execution_time_seconds=2.1)

        assert scorecard.overall_score == 100.0
        assert scorecard.certification_tier == SecurityCertificationTier.ENTERPRISE_SECURITY_READY
        assert scorecard.status == VerificationStatus.PASSED
        assert len(scorecard.categories) == 8
        for cat_name, cat in scorecard.categories.items():
            assert cat.score == 100.0

    def test_scorer_partial_failure(self):
        class FailingVerifier(IInfrastructureSecurityVerifier):
            @property
            def verifier_id(self) -> str:
                return "VERIFY-3N.3-CONTAINER-SEC"

            @property
            def name(self) -> str:
                return "Failing Container Security"

            def verify(self):
                return ContainerSecurityReport(
                    verifier_id="VERIFY-3N.3-CONTAINER-SEC",
                    phase_id="3N.3",
                    phase_name="Failing Container Security",
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
        scorer = InfrastructureSecurityScorer()
        scorecard = scorer.score([failing_report])
        assert scorecard.overall_score < 100.0
        assert scorecard.categories["Container Security"].score == 0.0

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Exporter & Manifest Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_exporter_generates_valid_json_and_sha256(self, temp_export_dir):
        exporter = InfrastructureSecurityExporter(export_dir=temp_export_dir)
        verifier = SecurityArchitectureVerifier()
        report = verifier.verify()
        written = exporter.export_report(report)
        assert len(written) > 0
        assert (Path(temp_export_dir) / "security_architecture_report.json").exists()

        scorer = InfrastructureSecurityScorer()
        scorecard = scorer.score([report])
        scorecard_written = exporter.export_scorecard(scorecard)
        assert len(scorecard_written) > 0
        assert (Path(temp_export_dir) / "security_scorecard.json").exists()

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
        runtime = InfrastructureSecurityRuntime()
        result = runtime.run_full_verification(export_dir=temp_export_dir)
        assert result["passed"] is True
        assert result["overall_score"] == 100.0
        assert result["tier"] == SecurityCertificationTier.ENTERPRISE_SECURITY_READY.value
        assert len(result["reports"]) == 16
        assert runtime.get_latest_scorecard() is not None
        assert runtime.get_latest_manifest() is not None

    def test_runtime_execute_verifier_lookup(self):
        runtime = InfrastructureSecurityRuntime()
        report1 = runtime.execute_verifier("3N.1")
        assert report1.phase_id == "3N.1"

        report6 = runtime.execute_verifier("VERIFY-3N.6-SECRET-SEC")
        assert report6.verifier_id == "VERIFY-3N.6-SECRET-SEC"

        with pytest.raises(ValueError):
            runtime.execute_verifier("INVALID-ID-999")

    # ──────────────────────────────────────────────────────────────────────────
    # 5. FastAPI REST Endpoints Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health(self, app_client):
        res = app_client.get("/api/v1/security/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"

    def test_api_phases(self, app_client):
        res = app_client.get("/api/v1/security/phases")
        assert res.status_code == 200
        phases = res.json()
        assert len(phases) == 16
        assert phases[0]["phase_id"] == "3N.1"

    def test_api_get_report(self, app_client):
        res = app_client.get("/api/v1/security/reports/3N.1")
        assert res.status_code == 200
        data = res.json()
        assert data["phase_id"] == "3N.1"
        assert data["score"] == 100.0

    def test_api_get_report_not_found(self, app_client):
        res = app_client.get("/api/v1/security/reports/NONEXISTENT")
        assert res.status_code == 404

    def test_api_run_verification(self, app_client):
        res = app_client.post("/api/v1/security/run")
        assert res.status_code == 200
        manifest = res.json()
        assert manifest["overall_score"] == 100.0
        assert manifest["certification_tier"] == "Enterprise Security Ready"
        assert len(manifest["files"]) > 0

    def test_api_scorecard(self, app_client):
        res = app_client.get("/api/v1/security/scorecard")
        assert res.status_code == 200
        scorecard = res.json()
        assert scorecard["overall_score"] == 100.0
        assert scorecard["status"] == "PASSED"

    def test_api_manifest(self, app_client):
        res = app_client.get("/api/v1/security/manifest")
        assert res.status_code == 200
        manifest = res.json()
        assert "files" in manifest
