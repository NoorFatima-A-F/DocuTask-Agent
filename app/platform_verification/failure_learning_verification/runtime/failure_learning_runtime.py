"""
Phase 3H.5.6: Failure Learning, RCA & Recovery Optimization Runtime
"""
from typing import Dict, Any, List
from ..verifiers import (
    FailureEventCollector,
    RootCauseEngine,
    PatternRecognitionVerifier,
    IncidentKnowledgeBase,
    RecoveryOptimizationEngine,
    PolicyImprovementVerifier,
    FailurePreventionVerifier,
    AutonomyGovernanceVerifier,
    FailureLearningSimulator,
)
from ..scoring.failure_learning_scorer import FailureLearningScorer
from ..exporter.failure_learning_exporter import FailureLearningExporter
from ..domain.models import FailureLearningScorecard


class FailureLearningRuntime:
    def __init__(self):
        self.collector = FailureEventCollector()
        self.rca_engine = RootCauseEngine()
        self.pattern_verifier = PatternRecognitionVerifier()
        self.kb_engine = IncidentKnowledgeBase()
        self.optimization_engine = RecoveryOptimizationEngine()
        self.policy_verifier = PolicyImprovementVerifier()
        self.prevention_verifier = FailurePreventionVerifier()
        self.autonomy_verifier = AutonomyGovernanceVerifier()
        self.simulator = FailureLearningSimulator()
        self.scorer = FailureLearningScorer()
        self.exporter = FailureLearningExporter()

    def run_full_failure_learning_verification(
        self, output_dir: str = "failure_learning_verification"
    ) -> Dict[str, Any]:
        event_report = self.collector.collect_failure_events()
        rca_report = self.rca_engine.analyze_root_causes()
        pattern_report = self.pattern_verifier.analyze_patterns()
        kb_report = self.kb_engine.build_knowledge_base()
        optimization_report = self.optimization_engine.optimize_recovery_decisions()
        policy_report = self.policy_verifier.evaluate_policy_improvements()
        prevention_report = self.prevention_verifier.verify_failure_prevention()
        autonomy_report = self.autonomy_verifier.verify_autonomy_matrix()
        simulation_report = self.simulator.run_simulation_tests()

        scorecard = self.scorer.calculate_scorecard(
            event_report=event_report,
            rca_report=rca_report,
            pattern_report=pattern_report,
            kb_report=kb_report,
            optimization_report=optimization_report,
            policy_report=policy_report,
            prevention_report=prevention_report,
            autonomy_report=autonomy_report,
            simulation_report=simulation_report,
        )

        exported_files = self.exporter.export_evidence_manifests(
            output_dir=output_dir,
            event_report=event_report,
            rca_report=rca_report,
            pattern_report=pattern_report,
            kb_report=kb_report,
            optimization_report=optimization_report,
            policy_report=policy_report,
            prevention_report=prevention_report,
            simulation_report=simulation_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "event_report": event_report,
            "rca_report": rca_report,
            "pattern_report": pattern_report,
            "kb_report": kb_report,
            "optimization_report": optimization_report,
            "policy_report": policy_report,
            "prevention_report": prevention_report,
            "autonomy_report": autonomy_report,
            "simulation_report": simulation_report,
            "exported_files": exported_files,
            "composite_score": scorecard.composite_score,
            "tier": scorecard.tier.value,
            "certified": scorecard.certified_enterprise_ready,
        }
