"""
Comprehensive Unit and Integration Tests for Phase 3H.5.6: Enterprise Failure Learning, Root Cause Analysis & Recovery Optimization.
"""
import os
import json
from app.platform_verification.failure_learning_verification.domain.models import (
    AutonomyLevel,
    KnowledgeCategory,
    IntelligenceTier,
)
from app.platform_verification.failure_learning_verification.verifiers.failure_event_collector import (
    FailureEventCollector,
)
from app.platform_verification.failure_learning_verification.verifiers.root_cause_engine import (
    RootCauseEngine,
)
from app.platform_verification.failure_learning_verification.verifiers.pattern_recognition_verifier import (
    PatternRecognitionVerifier,
)
from app.platform_verification.failure_learning_verification.verifiers.incident_knowledge_base import (
    IncidentKnowledgeBase,
)
from app.platform_verification.failure_learning_verification.verifiers.recovery_optimization_engine import (
    RecoveryOptimizationEngine,
)
from app.platform_verification.failure_learning_verification.verifiers.policy_improvement_verifier import (
    PolicyImprovementVerifier,
)
from app.platform_verification.failure_learning_verification.verifiers.failure_prevention_verifier import (
    FailurePreventionVerifier,
)
from app.platform_verification.failure_learning_verification.verifiers.autonomy_governance_verifier import (
    AutonomyGovernanceVerifier,
)
from app.platform_verification.failure_learning_verification.verifiers.failure_learning_simulator import (
    FailureLearningSimulator,
)
from app.platform_verification.failure_learning_verification.scoring.failure_learning_scorer import (
    FailureLearningScorer,
)
from app.platform_verification.failure_learning_verification.runtime.failure_learning_runtime import (
    FailureLearningRuntime,
)


class TestFailureLearningRecoveryVerification:
    """Test suite for validating Enterprise Failure Learning, Root Cause Analysis & Recovery Optimization components."""

    def test_failure_event_collector(self):
        collector = FailureEventCollector()
        report = collector.collect_failure_events()
        assert report.total_events_collected >= 5
        assert report.collection_pipeline_healthy is True
        assert len(report.events) == report.total_events_collected
        components = [e.component for e in report.events]
        assert "redis" in components
        assert "celery-worker-pool" in components
        assert "postgres-db" in components
        assert "gemini-ai-provider" in components

    def test_root_cause_engine(self):
        engine = RootCauseEngine()
        report = engine.analyze_root_causes()
        assert report.total_incidents_analyzed >= 4
        assert report.mean_rca_accuracy_pct >= 95.0
        assert report.rca_pipeline_valid is True
        for r in report.rca_records:
            assert r.confidence_score >= 0.95
            assert len(r.identified_root_cause) > 10

    def test_pattern_recognition_verifier(self):
        verifier = PatternRecognitionVerifier()
        report = verifier.analyze_patterns()
        assert report.total_patterns_detected >= 4
        assert report.pattern_recognition_accuracy_pct >= 95.0
        assert report.repeated_patterns_identified >= 3
        pattern_names = [p.pattern_name for p in report.patterns]
        assert any("OCR Native Heap Saturation" in name for name in pattern_names)
        assert any("DB Connection Leak" in name for name in pattern_names)

    def test_incident_knowledge_base(self):
        kb = IncidentKnowledgeBase()
        report = kb.build_knowledge_base()
        assert report.total_knowledge_articles >= 5
        assert report.retention_and_retrieval_healthy is True
        assert len(report.categories_covered) >= 5
        cats = [item.category for item in report.knowledge_items]
        assert KnowledgeCategory.INFRASTRUCTURE in cats
        assert KnowledgeCategory.APPLICATION in cats
        assert KnowledgeCategory.AI_PIPELINE in cats
        assert KnowledgeCategory.DEPENDENCY in cats
        assert KnowledgeCategory.SECURITY in cats

    def test_recovery_optimization_engine(self):
        engine = RecoveryOptimizationEngine()
        report = engine.optimize_recovery_decisions()
        assert report.total_optimizations_evaluated >= 4
        assert report.average_mttr_reduction_pct >= 95.0
        assert report.recovery_success_rate_pct == 100.0
        for opt in report.optimizations:
            assert opt.optimized_mttr_seconds < opt.previous_mttr_seconds
            assert opt.mttr_reduction_pct >= 90.0

    def test_policy_improvement_verifier(self):
        verifier = PolicyImprovementVerifier()
        report = verifier.evaluate_policy_improvements()
        assert report.total_policies_refined >= 4
        assert report.all_policies_safety_approved is True
        for p in report.policy_updates:
            assert p.safety_validated is True
            assert p.rollback_supported is True
            assert p.circuit_breaker_enabled is True

    def test_failure_prevention_verifier(self):
        verifier = FailurePreventionVerifier()
        report = verifier.verify_failure_prevention()
        assert report.total_early_warnings_evaluated >= 4
        assert report.prevention_rate_pct == 100.0
        assert report.early_detection_successful is True
        for sig in report.prevention_signals:
            assert sig.failure_prevented is True

    def test_autonomy_governance_verifier(self):
        verifier = AutonomyGovernanceVerifier()
        report = verifier.verify_autonomy_matrix()
        assert report.safety_governance_enforced is True
        levels = [m.autonomy_level for m in report.matrix_entries]
        assert AutonomyLevel.FULLY_AUTOMATIC in levels
        assert AutonomyLevel.APPROVAL_REQUIRED in levels
        assert AutonomyLevel.MANUAL_ONLY in levels

    def test_failure_learning_simulator(self):
        sim = FailureLearningSimulator()
        report = sim.run_simulation_tests()
        assert report.total_scenarios_simulated == 4
        assert report.all_scenarios_passed is True
        for res in report.results:
            assert res.pattern_detected is True
            assert res.knowledge_extracted is True
            assert res.policy_adapted is True
            assert res.simulation_passed is True

    def test_failure_learning_scorer(self):
        collector = FailureEventCollector()
        rca_engine = RootCauseEngine()
        pattern_verifier = PatternRecognitionVerifier()
        kb_engine = IncidentKnowledgeBase()
        optimization_engine = RecoveryOptimizationEngine()
        policy_verifier = PolicyImprovementVerifier()
        prevention_verifier = FailurePreventionVerifier()
        autonomy_verifier = AutonomyGovernanceVerifier()
        simulator = FailureLearningSimulator()
        scorer = FailureLearningScorer()

        scorecard = scorer.calculate_scorecard(
            event_report=collector.collect_failure_events(),
            rca_report=rca_engine.analyze_root_causes(),
            pattern_report=pattern_verifier.analyze_patterns(),
            kb_report=kb_engine.build_knowledge_base(),
            optimization_report=optimization_engine.optimize_recovery_decisions(),
            policy_report=policy_verifier.evaluate_policy_improvements(),
            prevention_report=prevention_verifier.verify_failure_prevention(),
            autonomy_report=autonomy_verifier.verify_autonomy_matrix(),
            simulation_report=simulator.run_simulation_tests(),
        )

        assert scorecard.composite_score >= 95.0
        assert scorecard.tier == IntelligenceTier.ADAPTIVE_RELIABILITY_INTELLIGENCE_READY
        assert scorecard.certified_enterprise_ready is True

    def test_full_runtime_and_export(self, tmp_path):
        out_dir = str(tmp_path / "failure_learning_verification")
        runtime = FailureLearningRuntime()
        results = runtime.run_full_failure_learning_verification(output_dir=out_dir)

        assert results["composite_score"] >= 95.0
        assert results["certified"] is True
        assert results["tier"] == "Adaptive Reliability Intelligence Ready"
        assert len(results["exported_files"]) == 10

        for file_path in results["exported_files"]:
            assert os.path.exists(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
