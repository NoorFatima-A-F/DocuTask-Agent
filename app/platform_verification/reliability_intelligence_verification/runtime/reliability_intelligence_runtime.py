"""
Phase 3H.5.7: Reliability Intelligence Runtime
"""
from typing import Dict, Any, List
from ..verifiers import (
    ReliabilityDataCollector,
    ComponentScoreEngine,
    SystemHealthScoreEngine,
    SLOVerifier,
    ErrorBudgetManager,
    ReliabilityRiskAnalyzer,
    ResilienceRecommendationEngine,
    ChaosReliabilityValidator,
    ReliabilityTrendAnalyzer,
    ReliabilityGovernanceVerifier,
)
from ..scoring.reliability_intelligence_scorer import ReliabilityIntelligenceScorer
from ..exporter.reliability_intelligence_exporter import ReliabilityIntelligenceExporter


class ReliabilityIntelligenceRuntime:
    def __init__(self):
        self.collector = ReliabilityDataCollector()
        self.component_scorer = ComponentScoreEngine()
        self.system_health_engine = SystemHealthScoreEngine()
        self.slo_verifier = SLOVerifier()
        self.budget_manager = ErrorBudgetManager()
        self.risk_analyzer = ReliabilityRiskAnalyzer()
        self.rec_engine = ResilienceRecommendationEngine()
        self.chaos_validator = ChaosReliabilityValidator()
        self.trend_analyzer = ReliabilityTrendAnalyzer()
        self.governance_verifier = ReliabilityGovernanceVerifier()
        self.scorer = ReliabilityIntelligenceScorer()
        self.exporter = ReliabilityIntelligenceExporter()

    def run_full_reliability_verification(
        self, output_dir: str = "reliability_intelligence_verification"
    ) -> Dict[str, Any]:
        data_report = self.collector.collect_reliability_data()
        comp_report = self.component_scorer.calculate_component_scores(data_report)
        health_report = self.system_health_engine.calculate_system_health(comp_report)
        slo_report = self.slo_verifier.verify_slos()
        budget_report = self.budget_manager.evaluate_error_budgets()
        risk_report = self.risk_analyzer.analyze_reliability_risks()
        rec_report = self.rec_engine.generate_recommendations(risk_report)
        chaos_report = self.chaos_validator.run_chaos_validation()
        trend_report = self.trend_analyzer.analyze_reliability_trends()
        gov_report = self.governance_verifier.evaluate_governance(
            health_report=health_report,
            budget_report=budget_report,
            risk_report=risk_report,
        )

        scorecard = self.scorer.calculate_scorecard(
            data_report=data_report,
            comp_report=comp_report,
            health_report=health_report,
            slo_report=slo_report,
            budget_report=budget_report,
            risk_report=risk_report,
            rec_report=rec_report,
            chaos_report=chaos_report,
            trend_report=trend_report,
            gov_report=gov_report,
        )

        exported_files = self.exporter.export_evidence_manifests(
            output_dir=output_dir,
            data_report=data_report,
            comp_report=comp_report,
            health_report=health_report,
            slo_report=slo_report,
            budget_report=budget_report,
            risk_report=risk_report,
            rec_report=rec_report,
            chaos_report=chaos_report,
            trend_report=trend_report,
            gov_report=gov_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "data_report": data_report,
            "comp_report": comp_report,
            "health_report": health_report,
            "slo_report": slo_report,
            "budget_report": budget_report,
            "risk_report": risk_report,
            "rec_report": rec_report,
            "chaos_report": chaos_report,
            "trend_report": trend_report,
            "gov_report": gov_report,
            "exported_files": exported_files,
            "composite_score": scorecard.composite_score,
            "overall_health_score": health_report.overall_health_score,
            "tier": scorecard.tier,
            "certified": scorecard.certified_enterprise_ready,
        }
