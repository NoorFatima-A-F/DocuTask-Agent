"""
Comprehensive Unit and Integration Tests for Phase 3H.5.7: Enterprise Reliability Intelligence, Health Scoring & Resilience Optimization.
"""
import os
import json
import pytest
from app.platform_verification.reliability_intelligence_verification.domain.models import (
    ErrorBudgetStatus,
    HealthScoreTier,
    SLOType,
    RiskLevel,
    RecommendationPriority,
    GovernanceAction,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.reliability_data_collector import (
    ReliabilityDataCollector,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.component_score_engine import (
    ComponentScoreEngine,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.system_health_score_engine import (
    SystemHealthScoreEngine,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.slo_verifier import (
    SLOVerifier,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.error_budget_manager import (
    ErrorBudgetManager,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.reliability_risk_analyzer import (
    ReliabilityRiskAnalyzer,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.resilience_recommendation_engine import (
    ResilienceRecommendationEngine,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.chaos_reliability_validator import (
    ChaosReliabilityValidator,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.reliability_trend_analyzer import (
    ReliabilityTrendAnalyzer,
)
from app.platform_verification.reliability_intelligence_verification.verifiers.reliability_governance_verifier import (
    ReliabilityGovernanceVerifier,
)
from app.platform_verification.reliability_intelligence_verification.scoring.reliability_intelligence_scorer import (
    ReliabilityIntelligenceScorer,
)
from app.platform_verification.reliability_intelligence_verification.runtime.reliability_intelligence_runtime import (
    ReliabilityIntelligenceRuntime,
)


class TestReliabilityIntelligenceVerification:
    """Test suite for validating Enterprise Reliability Intelligence, Health Scoring & Resilience Optimization components."""

    def test_reliability_data_collector(self):
        collector = ReliabilityDataCollector()
        report = collector.collect_reliability_data()
        assert report.total_components_monitored == 10
        assert report.collection_pipeline_healthy is True
        assert len(report.telemetry_items) == 10
        comps = [t.component for t in report.telemetry_items]
        assert "API Gateway" in comps
        assert "Agent Runtime" in comps
        assert "Planner" in comps
        assert "Execution Engine" in comps
        assert "Workers" in comps
        assert "Queue" in comps
        assert "Database" in comps
        assert "Storage" in comps
        assert "OCR Pipeline" in comps
        assert "AI Provider" in comps

    def test_component_score_engine(self):
        collector = ReliabilityDataCollector()
        scorer = ComponentScoreEngine()
        data_report = collector.collect_reliability_data()
        comp_report = scorer.calculate_component_scores(data_report)
        assert comp_report.total_components_scored == 10
        assert comp_report.mean_component_reliability_score >= 90.0
        for s in comp_report.component_scores:
            assert s.availability_score >= 90.0
            assert s.performance_score >= 85.0
            assert s.recovery_score >= 90.0
            assert s.stability_score >= 85.0
            assert s.composite_component_score >= 90.0

    def test_system_health_score_engine(self):
        collector = ReliabilityDataCollector()
        comp_engine = ComponentScoreEngine()
        health_engine = SystemHealthScoreEngine()
        comp_report = comp_engine.calculate_component_scores(collector.collect_reliability_data())
        health_report = health_engine.calculate_system_health(comp_report)
        assert health_report.overall_health_score >= 95.0
        assert health_report.health_tier == HealthScoreTier.EXCELLENT_RELIABILITY
        assert health_report.production_ready is True
        assert len(health_report.category_breakdown) == 6

    def test_slo_verifier(self):
        verifier = SLOVerifier()
        report = verifier.verify_slos()
        assert report.total_slos_evaluated == 4
        assert report.all_slos_met is True
        assert report.overall_slo_compliance_pct >= 95.0
        slo_types = [s.slo_type for s in report.slos]
        assert SLOType.AVAILABILITY in slo_types
        assert SLOType.LATENCY in slo_types
        assert SLOType.PROCESSING in slo_types
        assert SLOType.RECOVERY in slo_types

    def test_error_budget_manager(self):
        manager = ErrorBudgetManager()
        report = manager.evaluate_error_budgets()
        assert report.overall_budget_healthy is True
        assert report.budget_exhaustion_detected is False
        assert len(report.service_budgets) == 6
        for b in report.service_budgets:
            assert b.remaining_downtime_minutes > 0.0
            assert b.status in [ErrorBudgetStatus.HEALTHY, ErrorBudgetStatus.WARNING]

    def test_reliability_risk_analyzer(self):
        analyzer = ReliabilityRiskAnalyzer()
        report = analyzer.analyze_reliability_risks()
        assert report.total_risks_identified >= 4
        assert report.risk_analysis_valid is True
        for r in report.risks:
            assert r.probability_pct > 0.0
            assert len(r.lead_time_to_impact) > 0

    def test_resilience_recommendation_engine(self):
        analyzer = ReliabilityRiskAnalyzer()
        rec_engine = ResilienceRecommendationEngine()
        report = rec_engine.generate_recommendations(analyzer.analyze_reliability_risks())
        assert report.total_recommendations >= 4
        assert report.high_priority_count >= 2
        for r in report.recommendations:
            assert len(r.expected_impact) > 0
            assert len(r.effort_estimate) > 0

    def test_chaos_reliability_validator(self):
        validator = ChaosReliabilityValidator()
        report = validator.run_chaos_validation()
        assert report.total_chaos_tests == 4
        assert report.all_chaos_tests_passed is True
        for sc in report.scenarios:
            assert sc.resilience_validated is True
            assert sc.impact_contained is True
            assert sc.recovery_time_seconds < 10.0

    def test_reliability_trend_analyzer(self):
        analyzer = ReliabilityTrendAnalyzer()
        report = analyzer.analyze_reliability_trends()
        assert len(report.trends) == 3
        assert report.long_term_resilience_improving is True
        for t in report.trends:
            assert t.score_change_pct >= 0.0
            assert t.end_reliability_score >= t.start_reliability_score

    def test_reliability_governance_verifier(self):
        collector = ReliabilityDataCollector()
        comp_engine = ComponentScoreEngine()
        health_engine = SystemHealthScoreEngine()
        budget_manager = ErrorBudgetManager()
        risk_analyzer = ReliabilityRiskAnalyzer()
        gov_verifier = ReliabilityGovernanceVerifier()

        health_report = health_engine.calculate_system_health(
            comp_engine.calculate_component_scores(collector.collect_reliability_data())
        )
        budget_report = budget_manager.evaluate_error_budgets()
        risk_report = risk_analyzer.analyze_reliability_risks()

        gov_report = gov_verifier.evaluate_governance(
            health_report=health_report,
            budget_report=budget_report,
            risk_report=risk_report,
        )

        assert gov_report.deployment_gate_approved is True
        assert len(gov_report.governance_rules) == 3

    def test_reliability_intelligence_scorer(self):
        runtime = ReliabilityIntelligenceRuntime()
        results = runtime.run_full_reliability_verification()
        scorecard = results["scorecard"]

        assert scorecard.composite_score >= 95.0
        assert scorecard.tier == "Reliability Intelligence Certified"
        assert scorecard.certified_enterprise_ready is True

    def test_full_runtime_and_export(self, tmp_path):
        out_dir = str(tmp_path / "reliability_intelligence_verification")
        runtime = ReliabilityIntelligenceRuntime()
        results = runtime.run_full_reliability_verification(output_dir=out_dir)

        assert results["composite_score"] >= 95.0
        assert results["overall_health_score"] >= 95.0
        assert results["certified"] is True
        assert len(results["exported_files"]) == 12

        for file_path in results["exported_files"]:
            assert os.path.exists(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
