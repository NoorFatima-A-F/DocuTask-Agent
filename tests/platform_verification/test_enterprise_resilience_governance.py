"""
Comprehensive Test Suite for Part 3G.4:
Disaster Recovery Governance, Continuous Resilience Management & Operational Maturity Verification Framework.
"""
import pytest
import os
import json
import yaml
from pathlib import Path

from app.platform_verification.resilience_governance.domain.models import (
    ResilienceMaturityTier,
    GovernanceRiskSeverity,
    OwnershipValidationReport,
    PolicyValidationReport,
    RecoveryChangeImpactReport,
    DocumentationDriftReport,
    ResilienceMaturityScore,
    PostmortemSectionReport,
    ContinuousResilienceMetricsReport,
    GovernanceScorecard,
)
from app.platform_verification.resilience_governance.ownership.ownership_validator import (
    OwnershipValidator,
)
from app.platform_verification.resilience_governance.policies.policy_manager import (
    PolicyManager,
)
from app.platform_verification.resilience_governance.change_impact.change_impact_analyzer import (
    ChangeImpactAnalyzer,
)
from app.platform_verification.resilience_governance.drift_detection.doc_drift_detector import (
    DocumentationDriftDetector,
)
from app.platform_verification.resilience_governance.maturity.maturity_assessment_engine import (
    MaturityAssessmentEngine,
)
from app.platform_verification.resilience_governance.incidents.incident_lifecycle_verifier import (
    IncidentLifecycleVerifier,
)
from app.platform_verification.resilience_governance.metrics.continuous_resilience_metrics import (
    ContinuousResilienceMetricsEngine,
)
from app.platform_verification.resilience_governance.risk.resilience_risk_manager import (
    RiskCategory,
    RiskLevel,
    ResilienceRiskManager,
)
from app.platform_verification.resilience_governance.compliance_audit.audit_package_generator import (
    ComplianceAuditPackageGenerator,
)
from app.platform_verification.resilience_governance.review_pipeline.scheduled_review_engine import (
    ScheduledReviewEngine,
)
from app.platform_verification.resilience_governance.exporter.governance_exporter import (
    GovernanceExporter,
)
from app.platform_verification.resilience_governance.runtime.governance_runtime import (
    GovernanceRuntime,
)
from app.platform_verification.resilience_governance.api.governance_api import router
from fastapi.testclient import TestClient
from fastapi import FastAPI


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestEnterpriseResilienceGovernance:

    def test_ownership_validation_all_42_components_owned(self):
        validator = OwnershipValidator()
        report = validator.validate_ownership()

        assert report.total_components == 42
        assert report.owned_components == 42
        assert report.missing_owner == 0
        assert report.passed is True
        assert report.status == "PASS"

        # Verify YAML structure
        yaml_content = validator.generate_ownership_yaml()
        parsed = yaml.safe_load(yaml_content)
        assert parsed["total_components_cataloged"] == 42
        assert len(parsed["components"]) == 42
        for comp in parsed["components"]:
            assert comp["owner_role"] != ""
            assert comp["escalation_tier_1"] != ""
            assert comp["escalation_tier_2"] != ""
            assert comp["runbook_reference"] != ""

    def test_ownership_validation_orphaned_component_detection(self):
        validator = OwnershipValidator()
        # Simulate an unowned component on the instance
        validator.components_map.append(
            ("unowned-experimental-service", "", "Unknown", "", "", "")
        )
        report = validator.validate_ownership()
        assert report.missing_owner == 1
        assert report.passed is False
        assert report.status == "FAIL"

    def test_policy_manager_evaluates_all_4_dr_policies(self):
        manager = PolicyManager()
        report = manager.validate_policies()

        assert report.policies_evaluated == 4
        assert report.backup_policy_compliant is True
        assert report.restore_policy_compliant is True
        assert report.incident_policy_compliant is True
        assert report.testing_policy_compliant is True
        assert report.all_policies_enforced is True
        assert report.passed is True

        yamls = manager.generate_policy_yamls()
        assert "backup_policy" in yamls
        assert "restore_policy" in yamls
        assert "incident_policy" in yamls
        assert "testing_policy" in yamls

    def test_change_impact_analyzer_detects_uncovered_dependencies(self):
        analyzer = ChangeImpactAnalyzer()
        report = analyzer.analyze_change_impact()

        assert report.total_changes_scanned == 5
        assert report.uncovered_dependencies_count == 0
        assert report.passed is True

    def test_documentation_drift_detector_flags_drift(self):
        detector = DocumentationDriftDetector()
        report = detector.detect_documentation_drift()

        assert report.total_documents_scanned == 5
        assert report.drifts_detected_count == 0
        assert report.passed is True
        assert len(report.drift_items) == 5

    def test_incident_lifecycle_verifier_validates_5_sections(self):
        verifier = IncidentLifecycleVerifier()
        report = verifier.verify_incident_lifecycle()

        assert report.summary_valid is True
        assert report.timeline_valid is True
        assert report.root_cause_valid is True
        assert report.impact_valid is True
        assert report.action_items_valid is True
        assert report.postmortem_quality_score == 100.0
        assert report.passed is True
        assert len(report.action_items) == 4

        sections = verifier.generate_postmortem_markdown()
        assert "summary.md" in sections
        assert "timeline.md" in sections
        assert "root_cause.md" in sections
        assert "impact.md" in sections
        assert "action_items.md" in sections

    def test_continuous_resilience_metrics_sla_thresholds(self):
        engine = ContinuousResilienceMetricsEngine()
        report = engine.calculate_resilience_metrics()

        assert report.rto_average_minutes <= 15.0
        assert report.rpo_average_minutes <= 5.0
        assert report.mttr_average_minutes <= 20.0
        assert report.restore_success_rate_pct >= 99.0
        assert report.open_risks_count == 0
        assert report.overdue_actions_count == 0
        assert report.passed is True
        assert report.metrics_health_verdict == "EXEMPLARY_OPERATIONAL_HEALTH"

        prom = engine.generate_prometheus_metrics()
        assert "docutask_dr_rto_minutes" in prom
        assert "docutask_dr_restore_success_rate_pct" in prom

    def test_resilience_risk_manager_mitigations(self):
        manager = ResilienceRiskManager()
        report = manager.assess_risk_posture()

        assert report.total_risks_cataloged == 5
        assert report.high_critical_risks_unmitigated == 0
        assert report.passed is True

        categories = {r.category for r in report.risks}
        assert RiskCategory.INFRASTRUCTURE_DEPENDENCY in categories
        assert RiskCategory.DATA_INTEGRITY_AND_CORRUPTION in categories
        assert RiskCategory.SECURITY_AND_SECRETS in categories
        assert RiskCategory.OPERATIONAL_AND_HUMAN in categories
        assert RiskCategory.COMPLIANCE_AND_AUDIT in categories

    def test_compliance_audit_package_generator_and_checksums(self, tmp_path):
        generator = ComplianceAuditPackageGenerator()
        manifest = generator.evaluate_compliance()

        assert manifest.overall_compliance_pct == 100.0
        assert manifest.passed is True
        assert len(manifest.standards_evaluated) == 4

        audit_dir = tmp_path / "audit_test"
        files = generator.export_audit_package(str(audit_dir))
        assert len(files) >= 3
        assert (audit_dir / "audit_manifest.json").exists()
        assert (audit_dir / "certification" / "compliance_certificate.json").exists()

    def test_scheduled_review_engine_and_cicd_gate(self):
        engine = ScheduledReviewEngine()
        reviews = engine.evaluate_reviews()
        assert reviews["all_cadences_compliant"] is True
        assert reviews["total_cadences"] == 4

    def test_governance_runtime_full_execution_and_exports(self, tmp_path):
        runtime = GovernanceRuntime(
            base_dir=str(tmp_path),
            gov_dir_name="resilience_governance",
            audit_dir_name="audit_package",
            cert_dir_name="resilience_certification",
        )
        result = runtime.execute_governance_verification(export_artifacts=True)

        assert result.passed is True
        assert result.scorecard.overall_governance_score >= 95.0
        assert result.scorecard.certification_status == "ENTERPRISE_CERTIFIED"
        assert result.scorecard.ci_cd_deployment_approved is True
        assert result.maturity_score.maturity_level in [
            ResilienceMaturityTier.LEVEL_4_RESILIENT,
            ResilienceMaturityTier.LEVEL_5_ADAPTIVE,
        ]

        # Verify exported files
        assert (tmp_path / "resilience_governance" / "ownership" / "recovery_ownership.yaml").exists()
        assert (tmp_path / "resilience_governance" / "policies" / "backup_policy.yaml").exists()
        assert (tmp_path / "resilience_governance" / "metrics" / "metrics.prom").exists()
        assert (tmp_path / "resilience_governance" / "incidents" / "postmortems" / "root_cause.md").exists()
        assert (tmp_path / "resilience_certification" / "score.json").exists()
        assert (tmp_path / "resilience_certification" / "maturity_report.md").exists()
        assert (tmp_path / "resilience_certification" / "certification.json").exists()
        assert (tmp_path / "audit_package" / "audit_manifest.json").exists()

    def test_governance_api_endpoints(self, api_client):
        # 1. GET /status
        resp = api_client.get("/api/v1/governance/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["passed"] is True
        assert data["overall_score"] >= 95.0

        # 2. GET /ownership
        resp = api_client.get("/api/v1/governance/ownership")
        assert resp.status_code == 200
        assert resp.json()["total_components"] == 42
        assert resp.json()["missing_owner"] == 0

        # 3. GET /policies
        resp = api_client.get("/api/v1/governance/policies")
        assert resp.status_code == 200
        assert resp.json()["all_policies_enforced"] is True

        # 4. GET /metrics
        resp = api_client.get("/api/v1/governance/metrics")
        assert resp.status_code == 200
        assert resp.json()["rto_average_minutes"] <= 15.0

        # 5. GET /risks
        resp = api_client.get("/api/v1/governance/risks")
        assert resp.status_code == 200
        assert resp.json()["unmitigated_risks"] == 0

        # 6. GET /maturity
        resp = api_client.get("/api/v1/governance/maturity")
        assert resp.status_code == 200
        assert resp.json()["level_numeric"] >= 4

        # 7. POST /cicd-gate
        resp = api_client.post("/api/v1/governance/cicd-gate")
        assert resp.status_code == 200
        assert resp.json()["deployment_approved"] is True
