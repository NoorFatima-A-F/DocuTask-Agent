"""Reliability Intelligence Master Runtime.

Coordinates all 14 parts of the Phase 3H.3.7 Verification Framework.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone

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


class ReliabilityIntelligenceRuntime:
    """Master Orchestrator for Enterprise Reliability Engineering Intelligence Verification."""

    def __init__(self, export_dir: Optional[str] = None):
        self.model_verifier = ReliabilityModelVerifier()
        self.slo_verifier = SLOVerifier()
        self.error_budget_mgr = ErrorBudgetManager()
        self.pattern_analyzer = FailurePatternAnalyzer()
        self.root_cause_engine = RootCauseEngine()
        self.risk_scorer = ReliabilityRiskScorer()
        self.capacity_engine = CapacityIntelligenceEngine()
        self.change_analyzer = ChangeImpactAnalyzer()
        self.chaos_tracker = ChaosLearningTracker()
        self.recommender = ReliabilityRecommender()
        self.improvement_loop = ContinuousImprovementLoop()
        self.security_auditor = ReliabilitySecurityAuditor()
        self.maturity_scorer = ReliabilityMaturityScorer()
        self.exporter = ReliabilityEvidenceExporter(output_dir=export_dir)

    def run_full_verification(self) -> Dict[str, Any]:
        """Executes full end-to-end verification across all 14 reliability dimensions."""
        # 1. SLI / SLO Verification
        model_report = self.model_verifier.verify_reliability_model()
        slo_report = self.slo_verifier.verify_slos()
        budget_report = self.error_budget_mgr.evaluate_error_budgets()

        # 2. Analytics & Risk
        pattern_report = self.pattern_analyzer.analyze_rolling_patterns()
        rc_report = self.root_cause_engine.analyze_root_causes()
        risk_report = self.risk_scorer.compute_risk_scores(
            slo_report=slo_report,
            budget_report=budget_report,
            pattern_report=pattern_report,
        )

        # 3. Capacity & Change/Chaos
        capacity_report = self.capacity_engine.forecast_capacity()
        change_report = self.change_analyzer.analyze_releases()
        chaos_report = self.chaos_tracker.track_experiment_gains()

        # 4. Improvement & Recommendations
        rec_report = self.recommender.generate_recommendations(
            error_budget_report=budget_report,
            risk_report=risk_report,
            capacity_report=capacity_report,
            change_report=change_report,
        )
        loop_report = self.improvement_loop.evaluate_improvement_velocity()

        # 5. Security Audit
        sec_report = self.security_auditor.audit_security_controls()

        # 6. Maturity Scorecard Calculation
        scorecard = self.maturity_scorer.compute_scorecard(
            model_report=model_report,
            slo_report=slo_report,
            error_budget_report=budget_report,
            failure_pattern_report=pattern_report,
            root_cause_report=rc_report,
            risk_score_report=risk_report,
            capacity_report=capacity_report,
            change_impact_report=change_report,
            chaos_report=chaos_report,
            recommendation_report=rec_report,
            improvement_report=loop_report,
            security_report=sec_report,
        )

        # 7. Export Audit Evidence Manifests (11 files)
        exported_manifests = self.exporter.export_all(
            model_report=model_report,
            slo_report=slo_report,
            error_budget_report=budget_report,
            failure_pattern_report=pattern_report,
            root_cause_report=rc_report,
            risk_score_report=risk_report,
            capacity_report=capacity_report,
            change_impact_report=change_report,
            recommendation_report=rec_report,
            improvement_report=loop_report,
            security_report=sec_report,
            scorecard=scorecard,
        )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_report": model_report,
            "slo_report": slo_report,
            "error_budget_report": budget_report,
            "failure_pattern_report": pattern_report,
            "root_cause_report": rc_report,
            "risk_score_report": risk_report,
            "capacity_report": capacity_report,
            "change_impact_report": change_report,
            "chaos_report": chaos_report,
            "recommendation_report": rec_report,
            "improvement_report": loop_report,
            "security_report": sec_report,
            "scorecard": scorecard,
            "exported_manifests": exported_manifests,
            "passed": scorecard.passed,
        }
