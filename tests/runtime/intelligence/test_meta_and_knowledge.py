import pytest
from app.runtime.meta.regret import RegretEngine
from app.runtime.meta.exploration import ExplorationEngine
from app.runtime.meta.planner_critic import PlannerCritic
from app.runtime.meta.meta_planner import MetaPlanner
from app.runtime.knowledge.experience_graph import CausalExperienceGraph
from app.runtime.knowledge.policy_library import PolicyLibrary
from app.runtime.knowledge.knowledge_distillation import KnowledgeDistillationEngine


def test_regret_engine_computation():
    regret_engine = RegretEngine()
    analysis = regret_engine.compute_regret(
        mission_id="m_regret_test",
        chosen_strategy_id="strat_beta",
        strategy_utilities={"strat_alpha": 0.35, "strat_beta": 0.42, "strat_delta": 0.44},
        strategy_costs={"strat_alpha": 0.001, "strat_beta": 0.003, "strat_delta": 0.002},
    )
    
    assert analysis.chosen_strategy_id == "strat_beta"
    assert analysis.optimal_strategy_id == "strat_delta"
    assert analysis.expected_regret == 0.02
    assert analysis.opportunity_cost_usd >= 0


def test_exploration_engine_ucb1_and_thompson():
    bandit = ExplorationEngine()
    
    # Update some rewards
    bandit.update_arm_reward("strat_delta", reward=0.92)
    bandit.update_arm_reward("strat_beta", reward=0.88)
    
    selected_ucb1 = bandit.select_arm_ucb1()
    assert selected_ucb1.selected_arm_id in ["strat_alpha", "strat_beta", "strat_gamma", "strat_delta"]
    assert selected_ucb1.algorithm == "UCB1"
    
    selected_thompson = bandit.select_arm_thompson_sampling()
    assert selected_thompson.selected_arm_id in ["strat_alpha", "strat_beta", "strat_gamma", "strat_delta"]
    assert selected_thompson.algorithm == "ThompsonSampling"


def test_planner_critic_and_meta_planner():
    meta_planner = MetaPlanner()
    
    review = meta_planner.evaluate_and_supervise(
        mission_id="mission_complex_ocr_001",
        chosen_strategy_id="strat_delta",
        strategy_utilities={"strat_alpha": 0.31, "strat_delta": 0.4392},
        strategy_costs={"strat_alpha": 0.001, "strat_delta": 0.0022},
        estimated_risk=0.04,
        confidence=0.98,
        document_complexity=1.2,
    )
    
    assert review.mission_id == "mission_complex_ocr_001"
    assert review.critique.critique_score >= 0.0
    assert review.regret.expected_regret >= 0.0
    assert review.meta_verdict in ["ACCEPT_PLAN", "DEEPEN_SEARCH", "SWITCH_ALGORITHM"]


def test_experience_graph_and_knowledge_distillation():
    exp_graph = CausalExperienceGraph()
    exp_graph.record_experience(
        mission_id="mission_101",
        document_signature="inv_financial_p5",
        strategy_archetype="DELTA_PARETO",
        observed_latency_ms=1900.0,
        observed_cost_usd=0.0038,
        observed_accuracy=0.988,
        success=True,
    )
    
    policy_lib = PolicyLibrary()
    distiller = KnowledgeDistillationEngine(policy_library=policy_lib)
    report = distiller.distill_policy_from_graph(experience_graph=exp_graph)
    assert report.traces_analyzed > 0
    assert report.distilled_policy is not None
