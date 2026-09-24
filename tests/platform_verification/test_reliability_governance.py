"""
Test Suite: Phase 3I.6 Observability Governance, SLO Engineering & Reliability Certification
"""
import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.reliability_governance.domain.models import (
    SLIType,
    ErrorBudgetAction,
    ReliabilityCertificationTier,
    ReliabilityGovernanceReport,
    SLIReport,
    SLOReport,
    ErrorBudgetReport,
    ReliabilityDashboardReport,
    ReliabilityTrendReport,
    ProductionGateReport,
    ReliabilityRegressionReport,
    TelemetryQualityReport,
    ReliabilityAutomationReport,
    ReliabilityCertificationReport,
)

from app.platform_verification.reliability_governance.verifiers.governance_architecture_verifier import (
    GovernanceArchitectureVerifier,
)
from app.platform_verification.reliability_governance.verifiers.sli_definition_verifier import (
    SLIDefinitionVerifier,
)
from app.platform_verification.reliability_governance.verifiers.slo_engineering_verifier import (
    SLOEngineeringVerifier,
)
from app.platform_verification.reliability_governance.verifiers.error_budget_verifier import (
    ErrorBudgetVerifier,
)
from app.platform_verification.reliability_governance.verifiers.reliability_dashboard_verifier import (
    ReliabilityDashboardVerifier,
)
from app.platform_verification.reliability_governance.verifiers.reliability_trend_verifier import (
    ReliabilityTrendVerifier,
)
from app.platform_verification.reliability_governance.verifiers.production_readiness_gate_verifier import (
    ProductionReadinessGateVerifier,
)
from app.platform_verification.reliability_governance.verifiers.reliability_regression_verifier import (
    ReliabilityRegressionVerifier,
)
from app.platform_verification.reliability_governance.verifiers.telemetry_quality_verifier import (
    TelemetryQualityVerifier,
)
from app.platform_verification.reliability_governance.verifiers.reliability_automation_verifier import (
    ReliabilityAutomationVerifier,
)
from app.platform_verification.reliability_governance.scoring.reliability_quality_scorer import (
    ReliabilityQualityScorer,
)
from app.platform_verification.reliability_governance.runtime.reliability_governance_runtime import (
    ReliabilityGovernanceRuntime,
)
from app.platform_verification.reliability_governance.api.reliability_governance_api import (
    router as reliability_router,
)


# ─── 1. Verifier Tests ────────────────────────────────────────────────────────

def test_governance_architecture_verifier():
    verifier = GovernanceArchitectureVerifier()
    report = verifier.verify_governance_architecture()

    assert isinstance(report, ReliabilityGovernanceReport)
    assert report.services_monitored == 8
    assert len(report.ownership_boundaries) == 8
    assert report.slo_defined is True
    assert report.ownership_mapping is True
    assert report.user_journey_reliability_model_active is True
    assert report.status == "PASS"


def test_sli_definition_verifier():
    verifier = SLIDefinitionVerifier()
    report = verifier.verify_slis()

    assert isinstance(report, SLIReport)
    assert len(report.slis) >= 4
    assert report.all_slis_measured is True
    assert report.user_journey_coverage_pct == 100.0

    sli_types = {sli.sli_type for sli in report.slis}
    assert SLIType.AVAILABILITY in sli_types
    assert SLIType.LATENCY in sli_types
    assert SLIType.AI_QUALITY in sli_types
    assert SLIType.QUEUE_RELIABILITY in sli_types


def test_slo_engineering_verifier():
    verifier = SLOEngineeringVerifier()
    report = verifier.verify_slos()

    assert isinstance(report, SLOReport)
    assert len(report.slos) >= 4
    assert report.all_slos_compliant is True
    assert report.overall_compliance_pct == 100.0

    for slo in report.slos:
        assert slo.target_pct >= 95.0
        assert len(slo.owner) > 0
        assert slo.compliant is True


def test_error_budget_verifier():
    verifier = ErrorBudgetVerifier()
    report = verifier.verify_error_budgets()

    assert isinstance(report, ErrorBudgetReport)
    assert len(report.budgets) >= 4
    assert report.deployment_freeze_required is False
    assert report.average_remaining_budget_pct >= 50.0

    for budget in report.budgets:
        assert budget.total_budget_pct > 0
        assert budget.burn_rate_1h >= 0
        assert budget.burn_rate_6h >= 0
        assert budget.burn_rate_24h >= 0
        assert isinstance(budget.recommended_action, ErrorBudgetAction)


def test_reliability_dashboard_verifier():
    verifier = ReliabilityDashboardVerifier()
    report = verifier.verify_reliability_dashboards()

    assert isinstance(report, ReliabilityDashboardReport)
    assert len(report.views) >= 4
    assert report.dashboards_verified is True
    view_names = [v.view_name for v in report.views]
    assert any("System Health" in name for name in view_names)
    assert any("SLO" in name for name in view_names)
    assert any("AI" in name for name in view_names)
    assert any("Infrastructure" in name for name in view_names)


def test_reliability_trend_verifier():
    verifier = ReliabilityTrendVerifier()
    report = verifier.verify_reliability_trends()

    assert isinstance(report, ReliabilityTrendReport)
    assert len(report.trends) >= 5
    assert report.gradual_degradation_detected is False
    assert report.trend_stability_pct >= 95.0


def test_production_readiness_gate_verifier():
    verifier = ProductionReadinessGateVerifier()
    report = verifier.verify_production_gates()

    assert isinstance(report, ProductionGateReport)
    assert len(report.gates) >= 5
    assert report.deployment_approved is True
    assert report.pre_vs_post_slo_regression_detected is False


def test_reliability_regression_verifier():
    verifier = ReliabilityRegressionVerifier()
    report = verifier.verify_reliability_regression()

    assert isinstance(report, ReliabilityRegressionReport)
    assert len(report.regression_tests) >= 5
    assert report.all_tests_passed is True
    assert report.zero_regression_verified is True


def test_telemetry_quality_verifier():
    verifier = TelemetryQualityVerifier()
    report = verifier.verify_telemetry_quality()

    assert isinstance(report, TelemetryQualityReport)
    assert len(report.audits) == 3
    assert report.data_quality_score_pct >= 98.0


def test_reliability_automation_verifier():
    verifier = ReliabilityAutomationVerifier()
    report = verifier.verify_reliability_automation()

    assert isinstance(report, ReliabilityAutomationReport)
    assert len(report.rules) >= 4
    assert report.automation_enforced is True


# ─── 2. Scorer Tests ─────────────────────────────────────────────────────────

def test_reliability_quality_scorer():
    gov_verifier = GovernanceArchitectureVerifier()
    sli_verifier = SLIDefinitionVerifier()
    slo_verifier = SLOEngineeringVerifier()
    budget_verifier = ErrorBudgetVerifier()
    dash_verifier = ReliabilityDashboardVerifier()
    trend_verifier = ReliabilityTrendVerifier()
    gate_verifier = ProductionReadinessGateVerifier()
    reg_verifier = ReliabilityRegressionVerifier()
    qual_verifier = TelemetryQualityVerifier()
    auto_verifier = ReliabilityAutomationVerifier()

    scorer = ReliabilityQualityScorer()
    cert = scorer.calculate_certification_score(
        gov_report=gov_verifier.verify_governance_architecture(),
        sli_report=sli_verifier.verify_slis(),
        slo_report=slo_verifier.verify_slos(),
        budget_report=budget_verifier.verify_error_budgets(),
        dash_report=dash_verifier.verify_reliability_dashboards(),
        trend_report=trend_verifier.verify_reliability_trends(),
        gate_report=gate_verifier.verify_production_gates(),
        reg_report=reg_verifier.verify_reliability_regression(),
        qual_report=qual_verifier.verify_telemetry_quality(),
        auto_report=auto_verifier.verify_reliability_automation(),
    )

    assert isinstance(cert, ReliabilityCertificationReport)
    assert len(cert.pillar_scores) == 6
    assert cert.overall_score_pct >= 95.0
    assert cert.certification_granted is True
    assert cert.certification_tier == ReliabilityCertificationTier.ENTERPRISE_RELIABILITY_CERTIFIED

    # Verify pillar weights sum to 100%
    total_weights = sum(p.weight_pct for p in cert.pillar_scores)
    assert total_weights == 100.0


# ─── 3. Exporter & Artifact Verification ─────────────────────────────────────

def test_reliability_evidence_exporter(tmp_path):
    output_dir = str(tmp_path / "reliability_test_export")
    runtime = ReliabilityGovernanceRuntime(output_dir=output_dir)
    results = runtime.run_full_verification()

    assert results["status"] == "SUCCESS"
    assert os.path.exists(output_dir)

    expected_files = [
        "governance_report.json",
        "sli_report.json",
        "slo_report.json",
        "error_budget_report.json",
        "dashboard_report.json",
        "trend_analysis_report.json",
        "production_gate_report.json",
        "regression_report.json",
        "telemetry_quality_report.json",
        "automation_report.json",
        "certification_report.json",
        "metadata.json",
    ]

    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        assert os.path.exists(fpath), f"Missing expected evidence file: {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert len(data) > 0


# ─── 4. API Router Tests ─────────────────────────────────────────────────────

@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(reliability_router)
    return TestClient(app)


def test_api_run_verification(api_client):
    response = api_client.post("/api/v1/reliability-governance/run-verification")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["certification_granted"] is True
    assert data["overall_score_pct"] >= 95.0


def test_api_status(api_client):
    response = api_client.get("/api/v1/reliability-governance/status")
    assert response.status_code == 200
    data = response.json()
    assert data["certification_granted"] is True
    assert data["overall_score_pct"] >= 95.0
    assert len(data["pillar_scores"]) == 6


def test_api_error_budgets(api_client):
    response = api_client.get("/api/v1/reliability-governance/error-budgets")
    assert response.status_code == 200
    data = response.json()
    assert len(data["budgets"]) >= 4
    assert data["deployment_freeze_required"] is False


def test_api_slos(api_client):
    response = api_client.get("/api/v1/reliability-governance/slos")
    assert response.status_code == 200
    data = response.json()
    assert len(data["slos"]) >= 4
    assert data["all_slos_compliant"] is True
