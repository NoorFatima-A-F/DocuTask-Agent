"""Tests for Cost Predictor, Latency Predictor, Risk Intelligence, and Simulator."""

from app.runtime.planning.goal_engine import GoalUnderstandingEngine
from app.runtime.planning.constraint_engine import ConstraintExtractionEngine
from app.runtime.planning.capability_discovery import CapabilityDiscoveryEngine
from app.runtime.planning.strategy_generator import CandidateStrategyGenerator
from app.runtime.planning.cost_predictor import CostPredictionEngine
from app.runtime.planning.latency_predictor import LatencyPredictionEngine
from app.runtime.planning.risk_engine import RiskIntelligenceEngine
from app.runtime.planning.execution_simulator import ExecutionSimulator


def get_sample_strategy():
    caps = CapabilityDiscoveryEngine()
    goals = GoalUnderstandingEngine().parse_intent("m1", "Extract invoices")
    constraints = ConstraintExtractionEngine().extract_constraints("m1")
    gen = CandidateStrategyGenerator(caps)
    return gen.generate_strategies(goals, constraints)[0]


def test_cost_prediction_bounds():
    strategy = get_sample_strategy()
    engine = CostPredictionEngine()
    res = engine.predict_cost(strategy)

    assert res.total_cost_usd > 0
    assert res.ci_95_lower_usd <= res.total_cost_usd <= res.ci_95_upper_usd
    assert len(res.step_costs) == len(strategy.steps)


def test_latency_prediction_critical_path():
    strategy = get_sample_strategy()
    engine = LatencyPredictionEngine()
    res = engine.predict_latency(strategy, concurrency_limit=8)

    assert res.critical_path_ms > 0
    assert res.p50_ms <= res.p90_ms <= res.p95_ms <= res.p99_ms
    assert res.bottleneck_step_id is not None


def test_risk_intelligence_engine():
    strategy = get_sample_strategy()
    engine = RiskIntelligenceEngine()
    profile = engine.evaluate_strategy_risk(strategy, document_complexity=1.2)

    assert 0.0 <= profile.overall_risk_score <= 1.0
    assert len(profile.all_assessments) == 10
    assert len(profile.recommended_guardrails) > 0


def test_execution_simulator_monte_carlo():
    strategy = get_sample_strategy()
    sim = ExecutionSimulator(seed=123)
    res = sim.simulate(strategy, iterations=200)

    assert res.simulated_iterations == 200
    assert 0.0 <= res.simulated_success_rate <= 1.0
    assert res.mean_duration_ms > 0
    assert res.p95_duration_ms >= res.mean_duration_ms
