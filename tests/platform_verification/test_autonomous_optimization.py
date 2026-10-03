"""
Test Suite: Phase 3H.10 Autonomous Operational Intelligence & Self-Optimization Verification
"""
import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.autonomous_optimization.domain.models import (
    RiskTier,
    ExecutionMode,
    OptimizationActionType,
    AutonomousCertificationTier,
)

from app.platform_verification.autonomous_optimization.verifiers.operational_graph_verifier import (
    OperationalGraphVerifier,
)
from app.platform_verification.autonomous_optimization.verifiers.signal_correlation_verifier import (
    SignalCorrelationVerifier,
)
from app.platform_verification.autonomous_optimization.verifiers.trend_analysis_verifier import (
    TrendAnalysisVerifier,
)
from app.platform_verification.autonomous_optimization.verifiers.predictive_reliability_verifier import (
    PredictiveReliabilityVerifier,
)
from app.platform_verification.autonomous_optimization.verifiers.optimization_recommendation_verifier import (
    OptimizationRecommendationVerifier,
)
from app.platform_verification.autonomous_optimization.verifiers.autonomous_execution_verifier import (
    AutonomousExecutionVerifier,
)
from app.platform_verification.autonomous_optimization.verifiers.explainability_verifier import (
    ExplainabilityVerifier,
)
from app.platform_verification.autonomous_optimization.verifiers.learning_effectiveness_verifier import (
    LearningEffectivenessVerifier,
)
from app.platform_verification.autonomous_optimization.verifiers.governance_verifier import (
    GovernanceVerifier,
)

from app.platform_verification.autonomous_optimization.runtime.autonomous_optimization_runtime import (
    AutonomousOptimizationRuntime,
)
from app.platform_verification.autonomous_optimization.api.autonomous_optimization_api import (
    router,
)


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestOperationalGraph:
    def test_operational_graph_verification(self):
        verifier = OperationalGraphVerifier()
        report = verifier.verify_operational_graph()
        assert report.total_nodes >= 8
        assert report.total_edges >= 8
        assert report.graph_density > 0.0
        assert report.topology_valid is True
        assert len(report.critical_path_nodes) > 0
        assert any(n.node_id == "srv-api-gateway" for n in report.nodes)
        assert any(n.node_id == "srv-llm-router" for n in report.nodes)


class TestSignalCorrelation:
    def test_signal_correlation_verification(self):
        verifier = SignalCorrelationVerifier()
        report = verifier.verify_signal_correlation()
        assert report.total_clusters_formed >= 3
        assert report.mean_correlation_confidence >= 95.0
        assert report.correlation_accuracy_pct >= 98.0
        for cluster in report.clusters:
            assert len(cluster.signal_sources) >= 3
            assert cluster.correlation_confidence_pct >= 95.0


class TestTrendAnalysis:
    def test_trend_analysis_verification(self):
        verifier = TrendAnalysisVerifier()
        report = verifier.verify_trend_analysis()
        assert report.metrics_analyzed >= 5
        assert report.trend_stability_index >= 95.0
        for trend in report.trends:
            assert trend.projected_value_30d > 0.0
            assert trend.trajectory_direction in ["INCREASING", "DECREASING", "STABLE", "VOLATILE"]


class TestPredictiveReliability:
    def test_predictive_reliability_verification(self):
        verifier = PredictiveReliabilityVerifier()
        report = verifier.verify_predictive_reliability()
        assert report.total_risks_forecasted >= 3
        assert report.prediction_accuracy_pct >= 98.0
        for risk in report.risks:
            assert risk.probability_of_breach_pct > 0.0
            assert risk.estimated_time_to_incident_hours > 0.0
            assert isinstance(risk.mitigation_urgency, RiskTier)


class TestOptimizationRecommendations:
    def test_optimization_recommendations_verification(self):
        verifier = OptimizationRecommendationVerifier()
        report = verifier.verify_optimization_recommendations()
        assert report.total_recommendations >= 4
        assert report.recommendation_quality_score >= 98.0
        for rec in report.recommendations:
            assert isinstance(rec.action_type, OptimizationActionType)
            assert isinstance(rec.risk_tier, RiskTier)
            assert isinstance(rec.recommended_mode, ExecutionMode)
            assert len(rec.rollback_plan) > 10


class TestAutonomousExecutionSafety:
    def test_autonomous_execution_safety_verification(self):
        verifier = AutonomousExecutionVerifier()
        report = verifier.verify_autonomous_execution()
        assert report.actions_evaluated >= 4
        assert report.actions_cleared_for_autonomous_execution == report.actions_evaluated
        assert report.execution_safety_index >= 98.0
        for check in report.safety_checks:
            assert check.blast_radius_pct <= report.max_tolerated_blast_radius_pct
            assert check.maintenance_window_approved is True
            assert check.automated_rollback_verified is True


class TestExplainability:
    def test_explainability_verification(self):
        verifier = ExplainabilityVerifier()
        report = verifier.verify_explainability()
        assert report.decisions_explained >= 3
        assert report.explainability_index >= 98.0
        for trace in report.traces:
            assert len(trace.supporting_telemetry_evidence) >= 2
            assert len(trace.counterfactual_scenarios_evaluated) >= 2
            assert len(trace.human_readable_rationale) > 20


class TestLearningEffectiveness:
    def test_learning_effectiveness_verification(self):
        verifier = LearningEffectivenessVerifier()
        report = verifier.verify_learning_effectiveness()
        assert report.learning_cycles_evaluated >= 3
        assert report.cumulative_learning_gain_pct >= 95.0
        assert report.learning_effectiveness_score >= 98.0
        for cycle in report.cycles:
            assert cycle.positive_outcome_rate_pct >= 90.0
            assert cycle.false_optimization_rate_pct <= 5.0


class TestGovernance:
    def test_governance_verification(self):
        verifier = GovernanceVerifier()
        report = verifier.verify_governance()
        assert report.total_policies_checked >= 5
        assert report.compliance_rate_pct == 100.0
        assert report.immutable_ledger_verified is True
        for chk in report.audit_checks:
            assert chk.status == "COMPLIANT"
            assert len(chk.evidence_signature) == 64  # SHA-256 length


class TestAutonomousOptimizationScorer:
    def test_scorer_calculation(self):
        runtime = AutonomousOptimizationRuntime()
        res = runtime.run_full_verification(export_dir="autonomous_intelligence_verification_test")
        cert = res["certification_report"]
        assert cert.overall_score_pct >= 98.0
        assert cert.certification_tier == AutonomousCertificationTier.AUTONOMOUS_OPERATIONS_CERTIFIED
        assert cert.certification_granted is True
        assert len(cert.pillar_scores) == 7
        total_weight = sum(p.weight_pct for p in cert.pillar_scores)
        assert abs(total_weight - 100.0) < 0.01


class TestExporter:
    def test_evidence_exporter(self, tmp_path):
        runtime = AutonomousOptimizationRuntime()
        export_dir = str(tmp_path / "verification_artifacts")
        res = runtime.run_full_verification(export_dir=export_dir)
        meta = res["metadata"]

        assert meta["total_artifacts"] == 10
        assert len(meta["manifest_sha256"]) == 10

        for filename, expected_hash in meta["manifest_sha256"].items():
            filepath = os.path.join(export_dir, filename)
            assert os.path.exists(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)


class TestFastAPIRoutes:
    def test_all_endpoints(self, api_client):
        # /health
        res = api_client.get("/api/v1/autonomous-optimization/health")
        assert res.status_code == 200
        assert res.json()["status"] == "HEALTHY"

        # /verify
        res = api_client.post("/api/v1/autonomous-optimization/verify")
        assert res.status_code == 200
        assert res.json()["status"] == "COMPLETED"
        assert res.json()["overall_score_pct"] >= 98.0

        # /scorecard
        res = api_client.get("/api/v1/autonomous-optimization/scorecard")
        assert res.status_code == 200
        assert len(res.json()["pillar_scores"]) == 7

        # /graph
        res = api_client.get("/api/v1/autonomous-optimization/graph")
        assert res.status_code == 200
        assert res.json()["topology_valid"] is True

        # /correlations
        res = api_client.get("/api/v1/autonomous-optimization/correlations")
        assert res.status_code == 200
        assert res.json()["total_clusters_formed"] >= 3

        # /predictions
        res = api_client.get("/api/v1/autonomous-optimization/predictions")
        assert res.status_code == 200
        assert res.json()["total_risks_forecasted"] >= 3

        # /recommendations
        res = api_client.get("/api/v1/autonomous-optimization/recommendations")
        assert res.status_code == 200
        assert res.json()["total_recommendations"] >= 4

        # /safety
        res = api_client.get("/api/v1/autonomous-optimization/safety")
        assert res.status_code == 200
        assert res.json()["actions_evaluated"] >= 4

        # /governance
        res = api_client.get("/api/v1/autonomous-optimization/governance")
        assert res.status_code == 200
        assert res.json()["compliance_rate_pct"] == 100.0
