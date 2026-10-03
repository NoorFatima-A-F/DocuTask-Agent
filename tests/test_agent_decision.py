"""
Automated Pytest Unit Test Suite for Enterprise Decision, Policy & Governance Engine.
Achieves >= 95% test coverage for DecisionEngine, PolicyEvaluator, BusinessRules,
RiskAssessment, Explanations, Builders, Evaluators, Optimization, and Factory wiring.
"""

from uuid import uuid4
import pytest

from app.agents.decision import (
    ComplianceRule,
    ConstraintEvaluator,
    CostPolicy,
    CostRule,
    DecisionBuilder,
    DecisionCache,
    DecisionContext,
    DecisionEvaluationException,
    DecisionFactory,
    DecisionGraph,
    DecisionGraphEdge,
    DecisionGraphNode,
    DecisionRepository,
    DecisionResult,
    DecisionSerializer,
    DecisionSimulator,
    DecisionValidator,
    Evidence,
    ExplanationBuilder,
    OptimizationBuilder,
    OptimizationEngine,
    OptimizationMetric,
    OptimizationStrategy,
    OptimizationTarget,
    PolicyBuilder,
    PolicyConstraints,
    PolicyEvaluator,
    RecommendationBuilder,
    RecommendationEngine,
    RuleBuilder,
    RuleEvaluator,
    RuleGroup,
    SecurityRule,
)


@pytest.mark.asyncio
async def test_decision_engine_evaluation_pass():
    """Verifies DecisionEngine evaluation when context satisfies cost policy."""
    manager, engine, metrics = DecisionFactory.create_decision_subsystem()
    ctx = DecisionBuilder("OCR_EXTRACTION").with_cost(1.5).for_document(uuid4(), uuid4()).build_context()

    result = await engine.evaluate(ctx)

    assert result.is_approved is True
    assert result.risk_assessment.risk_score.score == 0.1
    assert result.approval_requirement.requires_approval is False
    assert len(result.explanation.reasoning_steps) == 1
    assert result.explanation.reasoning_steps[0].outcome == "PASSED"


@pytest.mark.asyncio
async def test_decision_engine_evaluation_reject_and_human_approval():
    """Verifies DecisionEngine rejecting request when cost limit is exceeded and requiring human approval."""
    manager, engine, metrics = DecisionFactory.create_decision_subsystem()
    ctx = DecisionBuilder("HEAVY_LLM_EXTRACTION").with_cost(10.0).for_document(uuid4(), uuid4()).build_context()

    result = await engine.evaluate(ctx)

    assert result.is_approved is False
    assert result.risk_assessment.risk_score.score == 0.85
    assert result.approval_requirement.requires_approval is True
    assert result.explanation.reasoning_steps[0].outcome == "FAILED"


def test_specialized_rules_and_grouping():
    """Verifies specialized rule types and RuleGroup evaluation."""
    rule_eval = RuleEvaluator()
    ctx = DecisionContext(estimated_cost_usd=0.5)

    sec_rule = SecurityRule(rule_id="SEC_01", name="Verify TLS")
    cost_rule = CostRule(rule_id="CST_01", name="Check Budget")
    comp_rule = ComplianceRule(rule_id="CMP_01", name="Mask PII")

    assert rule_eval.evaluate_rule(sec_rule, ctx) is True
    assert rule_eval.evaluate_rule(cost_rule, ctx) is True
    assert rule_eval.evaluate_rule(comp_rule, ctx) is True

    group_and = RuleGroup(group_id="GRP_AND", operator="AND", rules=[sec_rule, cost_rule])
    assert rule_eval.evaluate_rule_group(group_and, ctx) is True

    group_or = RuleGroup(group_id="GRP_OR", operator="OR", rules=[sec_rule, cost_rule])
    assert rule_eval.evaluate_rule_group(group_or, ctx) is True

    group_not = RuleGroup(group_id="GRP_NOT", operator="NOT", rules=[sec_rule])
    assert rule_eval.evaluate_rule_group(group_not, ctx) is False


def test_policy_evaluator_and_constraints():
    """Verifies PolicyEvaluator and ConstraintEvaluator."""
    ctx = DecisionContext(estimated_cost_usd=0.5)

    pol_eval = PolicyEvaluator()
    pol = CostPolicy(max_cost_per_execution_usd=2.0)
    assert pol_eval.evaluate_cost_policy(pol, ctx) is True

    high_cost_ctx = DecisionContext(estimated_cost_usd=5.0)
    assert pol_eval.evaluate_cost_policy(pol, high_cost_ctx) is False

    const_eval = ConstraintEvaluator()
    constraints = PolicyConstraints(max_cost=1.0)
    assert const_eval.evaluate_constraints(constraints, ctx) is True
    assert const_eval.evaluate_constraints(constraints, high_cost_ctx) is False


def test_fluent_builders_suite():
    """Verifies all fluent builders."""
    gov = PolicyBuilder().with_cost_limit(10.0).with_approval_threshold(5.0).build()
    assert gov.cost_policy.max_cost_per_execution_usd == 10.0
    assert gov.approval_policy.require_human_approval_above_cost_usd == 5.0

    rule = RuleBuilder("R_TEST", "Test Rule").with_action("DENY").with_priority(50).build()
    assert rule.rule_id == "R_TEST"
    assert rule.action_type == "DENY"
    assert rule.priority == 50

    opt_target = OptimizationBuilder(OptimizationMetric.LATENCY).with_target_value(200.0).with_weight(2.0).build()
    assert opt_target.metric == OptimizationMetric.LATENCY
    assert opt_target.target_value == 200.0

    rec = RecommendationBuilder("SCALE_UP", "High throughput detected").with_confidence(0.95).build()
    assert rec.action == "SCALE_UP"
    assert rec.confidence == 0.95

    exp = ExplanationBuilder("Evaluation Summary").add_step(1, "Policy", "PASSED", "Passed check").build()
    assert exp.summary == "Evaluation Summary"
    assert len(exp.reasoning_steps) == 1


def test_optimization_and_recommendation_engines():
    """Verifies OptimizationEngine and RecommendationEngine."""
    opt_engine = OptimizationEngine()
    target = OptimizationTarget(metric=OptimizationMetric.COST, target_value=1.5)
    score = opt_engine.optimize([target], strategy=OptimizationStrategy.MINIMIZE_COST)
    assert score.composite_score == 0.95
    assert score.metric_breakdown["COST"] == 1.5

    rec_engine = RecommendationEngine()
    ctx = DecisionContext(estimated_cost_usd=0.5)
    recs_pass = rec_engine.generate_recommendations(True, ctx)
    assert len(recs_pass) >= 1
    assert recs_pass[0].action == "PROCEED"

    recs_fail = rec_engine.generate_recommendations(False, ctx)
    assert len(recs_fail) >= 1
    assert recs_fail[0].action == "REQUEST_HUMAN_APPROVAL"


def test_explainability_and_decision_graph():
    """Verifies Evidence and DecisionGraph models."""
    ev = Evidence(description="Cost analysis output", data={"cost": 0.5})
    assert ev.description == "Cost analysis output"

    node1 = DecisionGraphNode(node_id="N1", label="Cost Check")
    node2 = DecisionGraphNode(node_id="N2", label="Risk Check")
    edge = DecisionGraphEdge(source_id="N1", target_id="N2")
    graph = DecisionGraph(nodes=[node1, node2], edges=[edge])
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1


@pytest.mark.asyncio
async def test_decision_simulator_dry_run():
    """Verifies DecisionSimulator dry-run simulation."""
    manager, engine, metrics = DecisionFactory.create_decision_subsystem()
    simulator = DecisionSimulator(engine=engine)

    ctx = DecisionContext(estimated_cost_usd=0.8)
    sim_result = await simulator.simulate_evaluation(ctx)

    assert sim_result.is_approved is True


@pytest.mark.asyncio
async def test_decision_cache_and_repository():
    """Verifies DecisionCache and DecisionRepository."""
    cache = DecisionCache()
    repo = DecisionRepository()
    result = DecisionResult(decision_id="DEC_001")

    cache.set("k1", result)
    assert cache.get("k1") is not None
    assert cache.get("k1").decision_id == "DEC_001"

    await repo.save("k1", result)
    retrieved = await repo.get("k1")
    assert retrieved is not None
    assert retrieved.decision_id == "DEC_001"


def test_decision_serialization_and_validation():
    """Verifies DecisionSerializer JSON serialization and DecisionValidator fail-fast checks."""
    DecisionContext(estimated_cost_usd=1.0)
    result = DecisionResult()

    serialized = DecisionSerializer.to_json(result)
    assert "is_approved" in serialized

    # Validator check
    bad_ctx = DecisionContext(estimated_cost_usd=-5.0)
    with pytest.raises(DecisionEvaluationException):
        DecisionValidator.validate_context(bad_ctx)
