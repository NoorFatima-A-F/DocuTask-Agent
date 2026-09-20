"""
Tests for Autonomous Scientific Intelligence & Continuous Research Platform (Phases 83C-95C)
==========================================================================================
Verifies Knowledge Graph, Memory, Recommendations, Hypothesis Generation, Planning,
Bayesian Optimization, Regression Detection, Observatory, Decision, Publication,
Governance, Scientific Agents, and Master Intelligence Engine.
"""

import math
import pytest
from typing import Dict, List

# 83C Knowledge Graph
from research_validation.knowledge_graph.ontology import EntityType, RelationshipType, ScientificOntology
from research_validation.knowledge_graph.knowledge_node import create_node
from research_validation.knowledge_graph.knowledge_graph import ScientificKnowledgeGraph
from research_validation.knowledge_graph.reasoning_engine import ScientificReasoningEngine

# 84C Memory
from research_validation.memory.experiment_memory import ExperimentMemoryStore
from research_validation.memory.failure_memory import FailureMemoryStore, FailureCategory
from research_validation.memory.success_memory import SuccessMemoryStore
from research_validation.memory.regression_memory import RegressionMemoryStore
from research_validation.memory.episodic_memory import EpisodicMemoryStore
from research_validation.memory.long_term_memory import LongTermMemoryStore
from research_validation.memory.memory_consolidation import ScientificMemoryConsolidator

# 85C Recommendation
from research_validation.recommendation.roi_calculator import ExperimentROICalculator
from research_validation.recommendation.uncertainty_sampler import UncertaintySampler
from research_validation.recommendation.recommendation_engine import ExperimentRecommendationEngine

# 86C Hypothesis
from research_validation.hypothesis.hypothesis_model import ScientificHypothesis
from research_validation.hypothesis.hypothesis_generator import AutonomousHypothesisGenerator
from research_validation.hypothesis.hypothesis_prioritizer import HypothesisPrioritizer

# 87C Planning
from research_validation.planning.execution_strategy import AdaptiveExecutionStrategy, TargetHardware
from research_validation.planning.adaptive_planner import AdaptiveExperimentPlanner

# 88C Optimization
from research_validation.optimization.gaussian_process import GaussianProcessRegressor
from research_validation.optimization.acquisition_functions import expected_improvement, upper_confidence_bound
from research_validation.optimization.bayesian_optimizer import BayesianResearchOptimizer, AcquisitionStrategy

# 89C Regression
from research_validation.regression.drift_detector import MultiDimensionalDriftDetector, DriftSeverity
from research_validation.regression.regression_detector import ScientificRegressionDetector

# 90C Observatory
from research_validation.observatory.benchmark_tracker import LivingBenchmarkTracker
from research_validation.observatory.leaderboard_tracker import LivingLeaderboardTracker
from research_validation.observatory.observatory_models import BenchmarkStatus

# 91C Decision
from research_validation.decision.decision_rules import ResearchAction
from research_validation.decision.research_decision_engine import ResearchDecisionEngine

# 92C Publication
from research_validation.publication.publication_evolution_engine import PublicationEvolutionEngine

# 93C Governance
from research_validation.governance.governance_policy import PolicyCategory
from research_validation.governance.governance_engine import ResearchGovernanceEngine

# 94C Scientific Agents
from research_validation.scientific_agents.agent_definitions import ScientificAgentRole
from research_validation.scientific_agents.scientific_agent_runtime import ScientificAgentRuntime

# 95C Master Orchestrator
from research_validation.scientific_runtime.scientific_intelligence_engine import ScientificIntelligenceEngine


def test_scientific_knowledge_graph_and_reasoning():
    kg = ScientificKnowledgeGraph()
    n_exp = kg.add_node("exp_1", EntityType.EXPERIMENT, "LayoutLMv3 Fine-tuning")
    n_ds = kg.add_node("ds_funsd", EntityType.DATASET, "FUNSD")
    n_met = kg.add_node("met_f1", EntityType.METRIC, "F1 Score")

    e1 = kg.add_relationship("exp_1", RelationshipType.EVALUATES, "ds_funsd")
    e2 = kg.add_relationship("exp_1", RelationshipType.PRODUCES_METRIC, "met_f1")

    assert len(kg.nodes) == 3
    assert len(kg.rel_engine.edges) == 2

    # Shortest path
    path = kg.query_engine.find_shortest_path("exp_1", "met_f1")
    assert path is not None
    assert len(path.nodes) == 2

    # Snapshot
    snap = kg.get_snapshot()
    assert snap.node_count == 3
    assert len(snap.root_digest_sha256) == 64

    # DOT export
    dot = kg.export_dot()
    assert "digraph ScientificKnowledgeGraph" in dot


def test_scientific_memory_engine_and_consolidation():
    exp_mem = ExperimentMemoryStore()
    fail_mem = FailureMemoryStore()
    succ_mem = SuccessMemoryStore()
    reg_mem = RegressionMemoryStore()
    epi_mem = EpisodicMemoryStore()
    lt_mem = LongTermMemoryStore()

    # Record experiment
    exp_entry = exp_mem.record_experiment("exp_01", "hash_01", {"lr": 1e-4}, {"f1": 0.95}, "COMPLETED", 120.0)
    assert exp_entry.metrics["f1"] == 0.95

    # Record failure
    fail_mem.record_failure("exp_02", FailureCategory.OUT_OF_MEMORY, {"batch_size": 128}, "CUDA OOM")
    is_known, matched = fail_mem.is_known_failure_configuration({"batch_size": 128, "model": "layoutlm"})
    assert is_known is True
    assert matched.category == FailureCategory.OUT_OF_MEMORY

    # Record success and Pareto front
    succ_mem.record_success("exp_01", {"lr": 1e-4}, {"accuracy": 0.96, "latency": 10.0}, 0.98)
    succ_mem.record_success("exp_03", {"lr": 2e-4}, {"accuracy": 0.92, "latency": 5.0}, 0.95)
    pareto = succ_mem.get_pareto_front("accuracy", "latency")
    assert len(pareto) >= 1

    # Long term memory retention decay
    lt_item = lt_mem.store_invariant("CONV_LAW", "Attention scales quadratically", evidence_weight=1.0, half_life_days=10.0)
    # Immediate retention
    assert lt_item.current_retention_strength(lt_item.created_timestamp) == 1.0
    # Decayed retention after 30 days
    decayed = lt_item.current_retention_strength(lt_item.created_timestamp + 30 * 86400)
    assert decayed < 0.5

    # Memory consolidation pass
    consolidator = ScientificMemoryConsolidator(epi_mem, fail_mem, succ_mem, lt_mem)
    rep = consolidator.consolidate()
    assert isinstance(rep.new_invariants_stored, int)


def test_experiment_recommendation_engine():
    calc = ExperimentROICalculator()
    roi = calc.calculate_roi("Bench_SROIE", prior_uncertainty_std=0.10, target_sample_size=100, estimated_runtime_sec=10.0)
    assert roi.expected_information_gain_bits > 0.0
    assert roi.net_roi_score > 0.0

    targets = UncertaintySampler.identify_gaps({"funsd": (10, 0.05), "sroie": (200, 0.01)})
    assert targets[0].target_name == "funsd"
    assert targets[0].priority_level == "HIGH"

    engine = ExperimentRecommendationEngine()
    recs = engine.generate_recommendations({"funsd": (10, 0.05)}, untested_hyperparameters=["weight_decay"])
    assert len(recs) >= 2
    assert recs[0].priority_score > 0.0


def test_hypothesis_generator_and_prioritizer():
    gen = AutonomousHypothesisGenerator()
    hypotheses = gen.generate_hypotheses({"f1": 0.88, "latency_p99_ms": 60.0}, ["funsd", "sroie"])
    assert len(hypotheses) >= 2

    prioritized = HypothesisPrioritizer.prioritize(hypotheses)
    assert len(prioritized) == len(hypotheses)
    assert prioritized[0].rank == 1
    assert prioritized[0].composite_priority_score >= prioritized[1].composite_priority_score
    assert prioritized[0].recommendation_verdict in ("EXECUTE_IMMEDIATELY", "SCHEDULE_NEXT", "DEFER")


def test_adaptive_experiment_planner():
    h = ScientificHypothesis(
        hypothesis_id="hyp_test",
        title="Test Hypothesis",
        statement="Pre-processing improves F1",
        premise="Low baseline F1",
        proposed_mechanism="Binarization",
        expected_outcome="F1 +2%",
        confidence_level=0.80,
        risk_score=0.10,
        impact_score=0.85,
        required_datasets=["funsd"],
        required_benchmarks=["ocr_bench"],
        estimated_runtime_sec=15.0,
        supporting_evidence_nodes=[],
    )
    plan = AdaptiveExperimentPlanner.build_plan(h)
    assert plan.plan_id.startswith("plan_hyp_test")
    assert plan.manifest.title.startswith("Plan: Test Hypothesis")
    assert len(plan.dependency_graph._nodes) == 7
    assert len(plan.plan_digest_sha256) == 64


def test_bayesian_research_optimizer():
    # Target objective: parabola with maximum at x = 0.75, f(0.75) = 1.0
    def objective(x: float) -> float:
        return -((x - 0.75) ** 2) + 1.0

    opt = BayesianResearchOptimizer(
        bounds=(0.0, 1.0),
        strategy=AcquisitionStrategy.EXPECTED_IMPROVEMENT,
        max_iterations=12,
        convergence_tolerance=1e-3,
        seed=42,
    )
    res = opt.optimize(objective, initial_points=[0.1, 0.9])
    assert res.total_steps > 2
    assert abs(res.best_x - 0.75) < 0.15  # within proximity of optimum
    assert res.best_y > 0.95
    assert len(res.optimization_digest_sha256) == 64


def test_scientific_regression_detector():
    detector = ScientificRegressionDetector()
    baseline = {"f1": 0.95, "latency_p50_ms": 10.0}
    
    # Degraded run
    eval_degraded = {"f1": 0.88, "latency_p50_ms": 25.0}
    rep_deg = detector.evaluate_experiment_regression("exp_reg", "run_base", "run_eval", baseline, eval_degraded)
    assert rep_deg.total_regressions_detected >= 1
    assert "BLOCK_RELEASE" in rep_deg.recommended_action or "FLAG_REVIEW" in rep_deg.recommended_action

    # Stable run
    eval_stable = {"f1": 0.955, "latency_p50_ms": 9.8}
    rep_stable = detector.evaluate_experiment_regression("exp_stab", "run_base", "run_eval2", baseline, eval_stable)
    assert rep_stable.total_regressions_detected == 0
    assert rep_stable.has_critical_regression is False


def test_living_benchmark_observatory_and_leaderboard():
    tracker = LivingBenchmarkTracker()
    records = tracker.audit_benchmark_availability()
    assert len(records) >= 5
    # Since benchmark directories are not yet populated on disk, verify DATASET_UNAVAILABLE fallback
    for r in records:
        assert r.status in (BenchmarkStatus.ACTIVE, BenchmarkStatus.DATASET_UNAVAILABLE)

    board = LivingLeaderboardTracker()
    ranked = board.record_standing("funsd", "LayoutLMv3", "3.0", 0.945)
    assert len(ranked) == 1
    assert ranked[0].rank == 1
    ranked2 = board.record_standing("funsd", "DocTrV2", "2.1", 0.960)
    assert ranked2[0].model_name == "DocTrV2"
    assert ranked2[0].rank == 1
    assert ranked2[1].rank == 2


def test_research_decision_engine():
    engine = ResearchDecisionEngine(max_acceptable_risk=0.80)
    
    # Normal hypothesis
    h_ok = ScientificHypothesis(
        hypothesis_id="h1", title="T1", statement="S1", premise="P1", proposed_mechanism="M1", expected_outcome="E1",
        confidence_level=0.85, risk_score=0.20, impact_score=0.90, required_datasets=["funsd"],
        required_benchmarks=[], estimated_runtime_sec=20.0, supporting_evidence_nodes=[],
    )
    d_ok = engine.evaluate_hypothesis(h_ok, available_datasets=["funsd"])
    assert d_ok.action == ResearchAction.RUN_EXPERIMENT

    # Missing dataset hypothesis
    d_missing = engine.evaluate_hypothesis(h_ok, available_datasets=[])
    assert d_missing.action == ResearchAction.NEED_MORE_DATASETS

    # Known failure match
    d_fail = engine.evaluate_hypothesis(h_ok, available_datasets=["funsd"], known_failure_match=True)
    assert d_fail.action == ResearchAction.REJECT_EXPERIMENT


def test_publication_evolution_engine():
    pub_engine = PublicationEvolutionEngine(base_version="1.0.0")
    draft1 = pub_engine.synthesize_draft(
        version="1.0.0",
        title="Scientific Report v1",
        claims={"Accuracy": "Baseline accuracy is 90%."},
        table_data={"Token_F1": {"baseline": 0.85, "observed": 0.90}},
        limitations=["English only"],
        evidence_digests={"Accuracy": "digest_001"},
    )
    assert draft1.version == "1.0.0"
    assert "Baseline accuracy is 90%" in draft1.markdown_content

    # Evolve publication
    draft2, diff_rep = pub_engine.evolve_publication(
        new_version="1.1.0",
        updated_claims={"Accuracy": "Enhanced accuracy reaches 95%."},
        updated_metrics={"Token_F1": {"baseline": 0.85, "observed": 0.95}},
        new_limitations=["English and French"],
        evidence_digests={"Accuracy": "digest_002"},
    )
    assert draft2.version == "1.1.0"
    assert diff_rep.has_significant_changes is True
    assert len(diff_rep.changes) >= 1


def test_research_governance_engine():
    gov = ResearchGovernanceEngine()
    
    # Compliant plan
    v_ok = gov.audit_experiment_plan("plan_01", has_provenance_digest=True, has_confidence_intervals=True)
    assert v_ok.is_fully_compliant is True
    assert v_ok.is_blocked is False
    assert len(v_ok.audit_root_digest) == 64

    # Non-compliant plan (missing provenance digest violates Zero Fabrication)
    v_bad = gov.audit_experiment_plan("plan_02", has_provenance_digest=False, has_confidence_intervals=True)
    assert v_bad.is_fully_compliant is False
    assert v_bad.is_blocked is True


def test_scientific_agent_runtime():
    runtime = ScientificAgentRuntime()
    assert len(runtime.agent_states) == 10
    
    verdict = runtime.run_collaborative_cycle("DocVQA multi-lingual generalization")
    assert verdict.consensus_reached is True
    assert len(verdict.participating_agents) == 10
    assert len(verdict.transcript_digest_sha256) == 64


def test_master_scientific_intelligence_engine():
    engine = ScientificIntelligenceEngine()
    mock_samples = [{"ground_truth_label": "total", "pred": {"label": "total"}}]
    
    result = engine.run_autonomous_cycle(cycle_number=1, mock_samples=mock_samples)
    assert result.cycle_id.startswith("research_cycle_1")
    assert result.selected_hypothesis is not None
    assert result.research_decision.action == ResearchAction.RUN_EXPERIMENT
    assert result.execution_result.status.value == "COMPLETED"
    assert result.governance_verdict.is_fully_compliant is True
    assert result.publication_draft.version == "2.1.0"
    assert len(result.next_cycle_recommendations) > 0
    assert len(result.cycle_digest_sha256) == 64
