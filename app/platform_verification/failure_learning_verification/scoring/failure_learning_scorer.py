"""
Phase 3H.5.6: Failure Learning, RCA & Recovery Optimization Scorer
"""
from typing import Dict, Any
from ..domain.interfaces import IFailureLearningScorer
from ..domain.models import (
    FailureLearningScorecard,
    IntelligenceTier,
    FailureEventReport,
    RootCauseReport,
    PatternAnalysisReport,
    KnowledgeBaseReport,
    RecoveryOptimizationReport,
    PolicyImprovementReport,
    FailurePreventionReport,
    AutonomyMatrixReport,
    SimulationReport,
)


class FailureLearningScorer(IFailureLearningScorer):
    def calculate_scorecard(
        self,
        event_report: FailureEventReport,
        rca_report: RootCauseReport,
        pattern_report: PatternAnalysisReport,
        kb_report: KnowledgeBaseReport,
        optimization_report: RecoveryOptimizationReport,
        policy_report: PolicyImprovementReport,
        prevention_report: FailurePreventionReport,
        autonomy_report: AutonomyMatrixReport,
        simulation_report: SimulationReport,
    ) -> FailureLearningScorecard:
        # 1. Failure analysis accuracy (25%)
        analysis_acc = 100.0 if (event_report.collection_pipeline_healthy and pattern_report.pattern_recognition_accuracy_pct >= 95.0) else 80.0

        # 2. Root cause identification (20%)
        rca_score = 100.0 if (rca_report.rca_pipeline_valid and rca_report.mean_rca_accuracy_pct >= 95.0) else 80.0

        # 3. Knowledge retention (15%)
        kb_score = 100.0 if (kb_report.retention_and_retrieval_healthy and len(kb_report.knowledge_items) >= 5) else 80.0

        # 4. Recovery optimization (20%)
        opt_score = 100.0 if (optimization_report.recovery_success_rate_pct >= 95.0 and policy_report.all_policies_safety_approved) else 80.0

        # 5. Prevention capability (15%)
        prev_score = 100.0 if (prevention_report.early_detection_successful and simulation_report.all_scenarios_passed) else 80.0

        # 6. Safety controls (5%)
        safety_score = 100.0 if autonomy_report.safety_governance_enforced else 80.0

        # Weighted calculation
        composite = (
            analysis_acc * 0.25
            + rca_score * 0.20
            + kb_score * 0.15
            + opt_score * 0.20
            + prev_score * 0.15
            + safety_score * 0.05
        )

        composite = round(composite, 2)

        if composite >= 95.0:
            tier = IntelligenceTier.ADAPTIVE_RELIABILITY_INTELLIGENCE_READY
            certified = True
        elif composite >= 90.0:
            tier = IntelligenceTier.ADVANCED_SELF_HEALING_READY
            certified = True
        elif composite >= 80.0:
            tier = IntelligenceTier.IMPROVEMENT_REQUIRED
            certified = False
        else:
            tier = IntelligenceTier.FAILED
            certified = False

        return FailureLearningScorecard(
            failure_analysis_accuracy=round(analysis_acc, 2),
            root_cause_score=round(rca_score, 2),
            knowledge_retention_score=round(kb_score, 2),
            recovery_optimization_score=round(opt_score, 2),
            prevention_capability_score=round(prev_score, 2),
            safety_controls_score=round(safety_score, 2),
            composite_score=composite,
            tier=tier,
            certified_enterprise_ready=certified,
        )
