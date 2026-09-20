"""Tests for Utility Calculation, Strategy Ranking, Pareto Frontier, and Counterfactual Reasoning."""

import pytest
from app.runtime.planning.goal_engine import GoalUnderstandingEngine
from app.runtime.planning.constraint_engine import ConstraintExtractionEngine
from app.runtime.planning.capability_discovery import CapabilityDiscoveryEngine
from app.runtime.planning.strategy_generator import CandidateStrategyGenerator
from app.runtime.planning.cost_predictor import CostPredictionEngine
from app.runtime.planning.latency_predictor import LatencyPredictionEngine
from app.runtime.planning.risk_engine import RiskIntelligenceEngine
from app.runtime.planning.utility_engine import MultiObjectiveUtilityEngine, UtilityWeights
from app.runtime.planning.strategy_ranker import StrategyRankingEngine
from app.runtime.planning.counterfactual_engine import CounterfactualEngine


@pytest.fixture
def planning_context():
    caps = CapabilityDiscoveryEngine()
    goals = GoalUnderstandingEngine().parse_intent("m_eval", "Extract multi-page invoice data")
    constraints = ConstraintExtractionEngine().extract_constraints("m_eval")
    gen = CandidateStrategyGenerator(caps)
    strategies = gen.generate_strategies(goals, constraints)

    cost_engine = CostPredictionEngine()
    lat_engine = LatencyPredictionEngine()
    risk_engine = RiskIntelligenceEngine()
    util_engine = MultiObjectiveUtilityEngine()

    c_map = {s.strategy_id: cost_engine.predict_cost(s) for s in strategies}
    l_map = {s.strategy_id: lat_engine.predict_latency(s) for s in strategies}
    r_map = {s.strategy_id: risk_engine.evaluate_strategy_risk(s) for s in strategies}
    u_map = {s.strategy_id: util_engine.calculate_utility(s, c_map[s.strategy_id], l_map[s.strategy_id], r_map[s.strategy_id]) for s in strategies}

    return {
        "strategies": strategies,
        "cost_map": c_map,
        "lat_map": l_map,
        "risk_map": r_map,
        "util_map": u_map,
        "util_engine": util_engine,
    }


def test_utility_equation_components(planning_context):
    strat = planning_context["strategies"][0]
    u_score = planning_context["util_map"][strat.strategy_id]

    assert -1.0 <= u_score.total_utility <= 1.0
    assert u_score.accuracy_term > 0
    assert u_score.latency_penalty_term >= 0
    assert u_score.cost_penalty_term >= 0
    assert u_score.risk_penalty_term >= 0


def test_strategy_ranking_and_pareto(planning_context):
    ranker = StrategyRankingEngine()
    res = ranker.evaluate_and_rank(
        mission_id="m_eval",
        strategies=planning_context["strategies"],
        utility_scores=planning_context["util_map"],
        cost_predictions=planning_context["cost_map"],
        latency_predictions=planning_context["lat_map"],
        risk_profiles=planning_context["risk_map"],
    )

    assert res.selected_strategy_id is not None
    assert len(res.comparison_matrix.entries) == 4
    assert len(res.comparison_matrix.pareto_frontier_strategy_ids) >= 1
    assert len(res.rejection_reasons) == 3


def test_counterfactual_engine_what_if(planning_context):
    cf_engine = CounterfactualEngine(planning_context["util_engine"])
    strategies = planning_context["strategies"]
    selected_id = strategies[0].strategy_id

    # Explain selection
    why_sel = cf_engine.explain_selection(
        selected_id,
        strategies,
        planning_context["util_map"],
        planning_context["cost_map"],
        planning_context["lat_map"],
        planning_context["risk_map"],
    )
    assert why_sel.query_type == "WHY_STRATEGY_SELECTED"
    assert len(why_sel.summary_explanation) > 10

    # What-if weight shift (latency priority)
    what_if = cf_engine.evaluate_what_if_weights(
        weight_overrides={"w_accuracy": 0.1, "w_latency": 0.8, "w_cost": 0.05, "w_risk": 0.05},
        strategies=strategies,
        cost_predictions=planning_context["cost_map"],
        latency_predictions=planning_context["lat_map"],
        risk_profiles=planning_context["risk_map"],
    )
    assert what_if.query_type == "WHAT_IF_WEIGHT_CHANGED"
    assert len(what_if.alternative_ranking) == 4
