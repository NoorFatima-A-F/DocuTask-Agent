"""
Comprehensive Unit and Integration Test Suite for Enterprise Backup Certification Framework.
Part 3G.2G — Backup Readiness Certification System for DocuTask Agent.
"""
import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.backup_certification.domain.models import (
    BackupCertificationTier,
)
from app.platform_verification.backup_certification.collector.evidence_collector import (
    EvidenceCollector,
)
from app.platform_verification.backup_certification.analyzers.completeness_analyzer import (
    CompletenessAnalyzer,
)
from app.platform_verification.backup_certification.analyzers.integrity_analyzer import (
    IntegrityAnalyzer,
)
from app.platform_verification.backup_certification.analyzers.restore_capability_analyzer import (
    RestoreCapabilityAnalyzer,
)
from app.platform_verification.backup_certification.analyzers.operational_readiness_analyzer import (
    OperationalReadinessAnalyzer,
)
from app.platform_verification.backup_certification.analyzers.rto_rpo_certifier import (
    RTORPOCertifier,
)
from app.platform_verification.backup_certification.policies.backup_policy_validator import (
    BackupPolicyValidator,
)
from app.platform_verification.backup_certification.validators.continuous_validation_engine import (
    ContinuousValidationEngine,
)
from app.platform_verification.backup_certification.risk.risk_register_generator import (
    RiskRegisterGenerator,
)
from app.platform_verification.backup_certification.scoring.backup_readiness_scoring_engine import (
    BackupReadinessScoringEngine,
)
from app.platform_verification.backup_certification.dashboard.backup_dashboard_engine import (
    BackupDashboardEngine,
)
from app.platform_verification.backup_certification.reports.certification_report_engine import (
    CertificationReportEngine,
)
from app.platform_verification.backup_certification.runtime.backup_certification_runtime import (
    BackupCertificationRuntime,
)
from app.platform_verification.backup_certification.api.backup_certification_api import (
    router,
)


@pytest.fixture
def app_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_evidence_collector():
    """Verify evidence collection across all 5 verification dimensions."""
    collector = EvidenceCollector()
    evidence = collector.collect_all_evidence()

    assert evidence is not None
    assert "backup_assets_count" in evidence.backup_inventory or "backup_assets" in evidence.backup_inventory
    assert evidence.restore_test_report.get("restore_success") is True
    assert evidence.integrity_report.get("checksum_validation") == "PASS"
    assert evidence.security_validation.get("passed") is True
    assert evidence.config_secrets_validation.get("passed") is True


def test_completeness_analyzer():
    """Verify completeness evaluation across 8 required enterprise asset classes."""
    collector = EvidenceCollector()
    evidence = collector.collect_all_evidence()
    analyzer = CompletenessAnalyzer()
    evaluation = analyzer.analyze_completeness(evidence)

    assert evaluation.database_verified is True
    assert evaluation.documents_verified is True
    assert evaluation.ocr_outputs_verified is True
    assert evaluation.extraction_results_verified is True
    assert evaluation.metadata_verified is True
    assert evaluation.configuration_verified is True
    assert evaluation.secrets_verified is True
    assert evaluation.infrastructure_state_verified is True
    assert evaluation.completeness_score == 100.0
    assert evaluation.passed is True
    assert len(evaluation.missing_assets) == 0


def test_integrity_analyzer():
    """Verify cryptographic integrity evaluation and tamper detection validation."""
    collector = EvidenceCollector()
    evidence = collector.collect_all_evidence()
    analyzer = IntegrityAnalyzer()
    evaluation = analyzer.analyze_integrity(evidence)

    assert evaluation.checksum_validation == "PASS"
    assert evaluation.corruption_detected is False
    assert evaluation.bit_flip_resilience_verified is True
    assert evaluation.digital_signatures_valid is True
    assert evaluation.integrity_score == 100.0
    assert evaluation.passed is True


def test_restore_capability_analyzer():
    """Verify restore success, duration, and data fidelity evaluation."""
    collector = EvidenceCollector()
    evidence = collector.collect_all_evidence()
    analyzer = RestoreCapabilityAnalyzer()
    evaluation = analyzer.analyze_restore_capability(evidence)

    assert evaluation.restore_success is True
    assert evaluation.rto_met is True
    assert evaluation.restore_duration_seconds <= 2700.0
    assert evaluation.recovered_data_accuracy_pct >= 99.9
    assert evaluation.dependency_recovery_verified is True
    assert evaluation.restore_capability_score == 100.0
    assert evaluation.passed is True


def test_operational_readiness_analyzer():
    """Verify operational readiness evaluation (automation, monitoring, alerting, runbooks)."""
    collector = EvidenceCollector()
    evidence = collector.collect_all_evidence()
    analyzer = OperationalReadinessAnalyzer()
    evaluation = analyzer.analyze_operational_readiness(evidence)

    assert evaluation.automation_enabled is True
    assert evaluation.monitoring_configured is True
    assert evaluation.alerts_configured is True
    assert evaluation.documentation_complete is True
    assert evaluation.ownership_assigned is True
    assert evaluation.operational_readiness_score == 100.0
    assert evaluation.passed is True


def test_rto_rpo_certifier():
    """Verify RTO (<= 45m) and RPO (<= 5m) certification and headroom calculations."""
    collector = EvidenceCollector()
    evidence = collector.collect_all_evidence()
    certifier = RTORPOCertifier()
    certification = certifier.certify_rto_rpo(evidence)

    assert certification.measured_rto_minutes <= 45.0
    assert certification.target_rto_minutes == 45.0
    assert certification.rto_status == "OPTIMAL_WITHIN_TARGET"
    assert certification.measured_rpo_minutes <= 5.0
    assert certification.target_rpo_minutes == 5.0
    assert certification.rpo_status == "OPTIMAL_WITHIN_TARGET"
    assert certification.rto_rpo_certified is True
    assert certification.passed is True


def test_backup_policy_validator():
    """Verify frequency and retention policy compliance across database, documents, and testing."""
    collector = EvidenceCollector()
    evidence = collector.collect_all_evidence()
    validator = BackupPolicyValidator()
    evaluation = validator.validate_policies(evidence)

    assert evaluation.database_frequency_compliant is True
    assert evaluation.database_retention_compliant is True
    assert evaluation.documents_frequency_compliant is True
    assert evaluation.documents_retention_compliant is True
    assert evaluation.restore_test_frequency_compliant is True
    assert evaluation.policy_compliance_score == 100.0
    assert evaluation.passed is True


def test_continuous_validation_schedule():
    """Verify daily, weekly, monthly, and quarterly scheduled jobs."""
    engine = ContinuousValidationEngine()
    schedule = engine.generate_verification_schedule()

    assert schedule.schedule_active is True
    assert schedule.daily_existence_check["assets_monitored"] == 245
    assert "SHA-512" in schedule.weekly_integrity_validation["algorithm"]
    assert "ISOLATED_DR_SANDBOX" in schedule.monthly_restore_test["environment"]
    assert len(schedule.quarterly_disaster_simulation["scenarios"]) == 3


def test_risk_register_generator():
    """Verify risk ledger generation and severity filtering."""
    collector = EvidenceCollector()
    evidence = collector.collect_all_evidence()
    completeness = CompletenessAnalyzer().analyze_completeness(evidence)
    integrity = IntegrityAnalyzer().analyze_integrity(evidence)
    restore = RestoreCapabilityAnalyzer().analyze_restore_capability(evidence)
    policy = BackupPolicyValidator().validate_policies(evidence)
    operational = OperationalReadinessAnalyzer().analyze_operational_readiness(evidence)

    generator = RiskRegisterGenerator()
    register = generator.generate_risk_register(completeness, integrity, restore, policy, operational)

    assert register.total_risks_identified >= 5
    assert register.critical_risks_count == 0
    assert register.high_risks_count == 0
    assert register.passed is True
    assert "ZERO UNMITIGATED" in register.summary


def test_backup_readiness_scoring_engine():
    """Verify weighted scoring calculation and tier assignment."""
    engine = BackupReadinessScoringEngine()

    # 1. Mission critical test
    scorecard_mc = engine.compute_certification_score(
        completeness_score=100.0,
        restore_score=100.0,
        integrity_score=100.0,
        security_score=100.0,
        automation_score=100.0,
        monitoring_score=100.0,
        documentation_score=100.0,
    )
    assert scorecard_mc.overall_score == 100.0
    assert scorecard_mc.certification_level == BackupCertificationTier.LEVEL_4_MISSION_CRITICAL_READY
    assert scorecard_mc.passed is True
    assert scorecard_mc.ci_cd_deployment_approved is True

    # 2. Enterprise ready test (92%)
    scorecard_ent = engine.compute_certification_score(
        completeness_score=90.0,
        restore_score=95.0,
        integrity_score=90.0,
        security_score=90.0,
        automation_score=90.0,
        monitoring_score=90.0,
        documentation_score=90.0,
    )
    assert 90.0 <= scorecard_ent.overall_score < 95.0
    assert scorecard_ent.certification_level == BackupCertificationTier.LEVEL_3_ENTERPRISE_READY
    assert scorecard_ent.ci_cd_deployment_approved is True

    # 3. Failed test (< 70%)
    scorecard_fail = engine.compute_certification_score(
        completeness_score=50.0,
        restore_score=50.0,
        integrity_score=50.0,
        security_score=50.0,
        automation_score=50.0,
        monitoring_score=50.0,
        documentation_score=50.0,
    )
    assert scorecard_fail.overall_score == 50.0
    assert scorecard_fail.certification_level == BackupCertificationTier.UNCERTIFIED_FAILED
    assert scorecard_fail.ci_cd_deployment_approved is False


def test_dashboard_engine():
    """Verify dashboard metrics generation."""
    collector = EvidenceCollector()
    evidence = collector.collect_all_evidence()
    rto_rpo = RTORPOCertifier().certify_rto_rpo(evidence)
    scorecard = BackupReadinessScoringEngine().compute_certification_score(
        100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0
    )

    dashboard_engine = BackupDashboardEngine()
    dashboard = dashboard_engine.generate_dashboard(scorecard, rto_rpo, evidence)

    assert dashboard.overall_score == 100.0
    assert dashboard.backup_health["status"] == "HEALTHY"
    assert dashboard.recovery_metrics["rto_measured_minutes"] <= 45.0
    assert len(dashboard.alerts_status) == 4


def test_certification_report_engine():
    """Verify artifact serialization to disk."""
    with tempfile.TemporaryDirectory() as tmpdir:
        collector = EvidenceCollector()
        evidence = collector.collect_all_evidence()
        completeness = CompletenessAnalyzer().analyze_completeness(evidence)
        integrity = IntegrityAnalyzer().analyze_integrity(evidence)
        restore = RestoreCapabilityAnalyzer().analyze_restore_capability(evidence)
        operational = OperationalReadinessAnalyzer().analyze_operational_readiness(evidence)
        rto_rpo = RTORPOCertifier().certify_rto_rpo(evidence)
        policy = BackupPolicyValidator().validate_policies(evidence)
        schedule = ContinuousValidationEngine().generate_verification_schedule()
        risks = RiskRegisterGenerator().generate_risk_register(
            completeness, integrity, restore, policy, operational
        )
        scorecard = BackupReadinessScoringEngine().compute_certification_score(
            100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0
        )
        dashboard = BackupDashboardEngine().generate_dashboard(scorecard, rto_rpo, evidence)

        report_engine = CertificationReportEngine(root_output_dir=tmpdir)
        manifests = report_engine.export_all_certification_artifacts(
            scorecard=scorecard,
            completeness=completeness,
            integrity=integrity,
            restore=restore,
            operational=operational,
            rto_rpo=rto_rpo,
            policy=policy,
            risks=risks,
            schedule=schedule,
            dashboard=dashboard,
            evidence=evidence,
            output_dir=tmpdir,
        )

        assert len(manifests) == 14
        for rel_path, abs_path in manifests.items():
            assert os.path.exists(abs_path), f"Missing artifact: {abs_path}"


def test_runtime_e2e_certification():
    """Verify master runtime orchestrator execution."""
    with tempfile.TemporaryDirectory() as tmpdir:
        runtime = BackupCertificationRuntime()
        results = runtime.execute_full_certification(output_dir=tmpdir)

        assert results["passed"] is True
        assert results["ci_cd_deployment_approved"] is True
        assert results["scorecard"].overall_score >= 95.0
        assert results["scorecard"].certification_level == BackupCertificationTier.LEVEL_4_MISSION_CRITICAL_READY
        assert len(results["manifests"]) == 14


def test_api_endpoints(app_client):
    """Verify all FastAPI router endpoints."""
    # 1. Certify endpoint
    resp = app_client.post("/api/v1/platform-verification/backup-certification/certify")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "COMPLETED"
    assert data["overall_score"] >= 90.0
    assert data["ci_cd_deployment_approved"] is True

    # 2. Scorecard endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-certification/scorecard")
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_score"] >= 90.0

    # 3. Dashboard endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-certification/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert data["backup_health"]["status"] == "HEALTHY"

    # 4. RTO/RPO endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-certification/rto-rpo")
    assert resp.status_code == 200
    data = resp.json()
    assert data["rto_rpo_certified"] is True

    # 5. Risk register endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-certification/risk-register")
    assert resp.status_code == 200
    data = resp.json()
    assert data["critical_risks_count"] == 0

    # 6. Continuous schedule endpoint
    resp = app_client.get("/api/v1/platform-verification/backup-certification/continuous-schedule")
    assert resp.status_code == 200
    data = resp.json()
    assert data["schedule_active"] is True
