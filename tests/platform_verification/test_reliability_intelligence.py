"""Test Suite for Phase 3H.3.7 - Enterprise Reliability Engineering Intelligence Verification Framework.

Tests all 14 parts (3H.3.7A to 3H.3.7N), API endpoints, runtime orchestration, and artifact generation.
"""

import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.reliability_intelligence.sli_slo.reliability_model_verifier import ReliabilityModelVerifier
from app.platform_verification.reliability_intelligence.sli_slo.slo_verifier import SLOVerifier
from app.platform_verification.reliability_intelligence.sli_slo.error_budget_manager import ErrorBudgetManager
from app.platform_verification.reliability_intelligence.analytics.failure_pattern_analyzer import FailurePatternAnalyzer
from app.platform_verification.reliability_intelligence.analytics.root_cause_engine import RootCauseEngine
from app.platform_verification.reliability_intelligence.analytics.reliability_risk_scorer import ReliabilityRiskScorer
from app.platform_verification.reliability_intelligence.capacity.capacity_intelligence_engine import CapacityIntelligenceEngine
from app.platform_verification.reliability_intelligence.change_chaos.change_impact_analyzer import ChangeImpactAnalyzer
from app.platform_verification.reliability_intelligence.change_chaos.chaos_learning_tracker import ChaosLearningTracker
from app.platform_verification.reliability_intelligence.improvement.reliability_recommender import ReliabilityRecommender
from app.platform_verification.reliability_intelligence.improvement.continuous_improvement_loop import ContinuousImprovementLoop
from app.platform_verification.reliability_intelligence.security.reliability_security_auditor import ReliabilitySecurityAuditor
from app.platform_verification.reliability_intelligence.scoring.reliability_maturity_scorer import ReliabilityMaturityScorer
from app.platform_verification.reliability_intelligence.exporter.reliability_evidence_exporter import ReliabilityEvidenceExporter
from app.platform_verification.reliability_intelligence.runtime.reliability_intelligence_runtime import ReliabilityIntelligenceRuntime
from app.platform_verification.reliability_intelligence.api.reliability_intelligence_api import router as reliability_router
from app.platform_verification.reliability_intelligence.domain.models import (
    ReliabilityMaturityTier,
    SLIType,
    RecommendationPriority,
)


def test_part_3h_3_7a_reliability_model_verifier():
    verifier = ReliabilityModelVerifier()
    report = verifier.verify_reliability_model()
    assert report.passed is True
    assert report.total_slis_defined >= 5
    assert report.measurement_coverage_pct >= 95.0
    # Check all critical services are covered
    services = {sli.service for sli in report.slis}
    assert "api_service" in services
    assert "document_pipeline" in services
    assert "agent_runtime" in services
    assert "gemini_ai_provider" in services


def test_part_3h_3_7b_slo_verifier_targets_and_attainment():
    verifier = SLOVerifier()
    report = verifier.verify_slos()
    assert report.passed is True
    assert report.total_slos_tracked >= 4
    assert report.slos_met_count == report.total_slos_tracked
    assert report.slo_compliance_pct == 100.0

    # Verify specific enterprise SLO targets
    slo_map = {slo.service: slo for slo in report.slos}
    assert slo_map["api_service"].target_pct == 99.5
    assert slo_map["document_pipeline"].target_pct == 99.0
    assert slo_map["agent_runtime"].target_pct == 98.0
    assert slo_map["gemini_ai_provider"].target_pct == 99.0


def test_part_3h_3_7c_error_budget_manager_and_policies():
    mgr = ErrorBudgetManager()
    report = mgr.evaluate_error_budgets()
    assert report.passed is True
    assert report.total_budgets_tracked >= 4
    assert report.deployment_freeze_active is False

    # Ensure remaining budget is calculated and > 0
    for budget in report.budgets:
        assert budget.remaining_budget_pct > 0.0
        assert budget.burn_rate_1h >= 0.0
        assert budget.policy_recommendation != ""


def test_part_3h_3_7d_failure_pattern_analyzer():
    analyzer = FailurePatternAnalyzer()
    report = analyzer.analyze_rolling_patterns()
    assert report.passed is True
    assert report.total_patterns_identified >= 3
    assert report.highest_risk_component != ""
    assert report.recurring_failures_detected > 0


def test_part_3h_3_7e_root_cause_engine():
    engine = RootCauseEngine()
    report = engine.analyze_root_causes()
    assert report.passed is True
    assert report.total_analyses >= 2
    assert report.avg_confidence_score >= 0.85
    for rca in report.analyses:
        assert rca.confidence_score >= 0.80
        assert rca.root_cause != ""


def test_part_3h_3_7f_reliability_risk_scorer():
    scorer = ReliabilityRiskScorer()
    report = scorer.compute_risk_scores()
    assert report.passed is True
    assert report.total_services_evaluated >= 4
    assert report.avg_composite_score >= 90.0
    for s in report.service_scores:
        assert 0.0 <= s.composite_score <= 100.0
        assert s.risk_tier in ("LOW", "MEDIUM", "HIGH")


def test_part_3h_3_7g_capacity_intelligence_engine():
    engine = CapacityIntelligenceEngine()
    report = engine.forecast_capacity()
    assert report.passed is True
    assert report.total_resources_monitored >= 4
    assert report.high_risk_exhaustion_count == 0
    for f in report.forecasts:
        assert f.projected_days_to_exhaustion >= 14.0


def test_part_3h_3_7h_change_impact_analyzer():
    analyzer = ChangeImpactAnalyzer()
    report = analyzer.analyze_releases()
    assert report.passed is True
    assert report.total_releases_analyzed >= 3
    assert report.regressions_detected == 0


def test_part_3h_3_7i_chaos_learning_tracker():
    tracker = ChaosLearningTracker()
    report = tracker.track_experiment_gains()
    assert report.passed is True
    assert report.total_experiments_tracked >= 4
    assert report.avg_mttr_improvement_pct >= 40.0
    for exp in report.experiments:
        assert exp.improvement_pct > 0.0


def test_part_3h_3_7j_reliability_recommender():
    recommender = ReliabilityRecommender()
    report = recommender.generate_recommendations()
    assert report.passed is True
    assert report.total_recommendations >= 4
    assert any(r.priority == RecommendationPriority.P0_CRITICAL for r in report.recommendations)
    assert any(r.priority == RecommendationPriority.P1_HIGH for r in report.recommendations)


def test_part_3h_3_7k_continuous_improvement_loop():
    loop = ContinuousImprovementLoop()
    report = loop.evaluate_improvement_velocity()
    assert report.passed is True
    assert report.total_cycles_reviewed >= 2
    assert report.improvement_velocity_active is True


def test_part_3h_3_7l_reliability_security_auditor():
    auditor = ReliabilitySecurityAuditor()
    report = auditor.audit_security_controls()
    assert report.passed is True
    assert report.pii_or_secrets_exposed is False
    assert report.access_control_active is True

    # Test detection of API key leaks
    leaks = auditor.scan_for_sensitive_data("Authorization: Bearer " + "sk-ant-" + "0" * 32)
    assert len(leaks) > 0


def test_part_3h_3_7m_evidence_exporter_and_11_manifests(tmp_path):
    output_dir = str(tmp_path / "verification_output")
    runtime = ReliabilityIntelligenceRuntime(export_dir=output_dir)
    res = runtime.run_full_verification()

    assert os.path.exists(output_dir)
    expected_files = [
        "reliability_model_report.json",
        "slo_report.json",
        "error_budget_report.json",
        "failure_pattern_report.json",
        "root_cause_report.json",
        "risk_score_report.json",
        "capacity_report.json",
        "change_impact_report.json",
        "recommendation_report.json",
        "improvement_report.json",
        "metadata.json",
    ]
    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        assert os.path.exists(fpath), f"Missing expected manifest file {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data is not None


def test_part_3h_3_7n_maturity_scorer_and_tier():
    runtime = ReliabilityIntelligenceRuntime()
    res = runtime.run_full_verification()
    scorecard = res["scorecard"]

    assert scorecard.passed is True
    assert scorecard.overall_score >= 95.0
    assert scorecard.certification_tier == ReliabilityMaturityTier.RELIABILITY_ENGINEERING_MATURE
    assert scorecard.certification_verdict == "CERTIFIED"


def test_reliability_intelligence_fastapi_endpoints():
    app = FastAPI()
    app.include_router(reliability_router)
    client = TestClient(app)

    endpoints = [
        "/health/reliability/model",
        "/health/reliability/slos",
        "/health/reliability/error-budgets",
        "/health/reliability/failure-patterns",
        "/health/reliability/root-causes",
        "/health/reliability/risk-scores",
        "/health/reliability/capacity",
        "/health/reliability/change-impact",
        "/health/reliability/chaos-learning",
        "/health/reliability/recommendations",
        "/health/reliability/improvement",
        "/health/reliability/security",
        "/health/reliability/scorecard",
    ]

    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200, f"Endpoint {ep} failed with status {resp.status_code}"
        assert resp.json() is not None

    # Test POST /health/reliability/verify
    post_resp = client.post("/health/reliability/verify")
    assert post_resp.status_code == 200
    data = post_resp.json()
    assert data["passed"] is True
    assert data["scorecard"]["overall_score"] >= 95.0
