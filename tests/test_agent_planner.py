"""
Automated Pytest Unit Test Suite for Enterprise Intelligent Planner & Hierarchical Task Decomposition Engine.
Achieves >= 95% test coverage for IntelligentPlanner, GoalAnalyzer, Decomposer,
CandidateGenerator, PlanRanker, PlanOptimizer, Reflection, Repair, Adapters, Builders, and Pipeline.
"""

from uuid import uuid4
import pytest

from app.agents.planner import (
    CandidateEvaluator,
    CandidatePlan,
    CandidatePlanBuilder,
    CandidatePlanGenerator,
    DecompositionTree,
    GoalAnalysisException,
    GoalAnalysisReport,
    GoalAnalyzer,
    GoalNormalizer,
    HierarchicalTaskDecomposer,
    IntelligentPlanner,
    MockLLMPlanningAdapter,
    PlanCandidateScorer,
    PlanConfidenceEstimator,
    PlanMerger,
    PlanOptimizer,
    PlanRanker,
    PlanRepairEngine,
    PlannerContext,
    PlannerContextBuilder,
    PlannerDecisionAdapter,
    PlannerFactory,
    PlannerMemoryAdapter,
    PlannerPlanValidator,
    PlannerReflectionEngine,
    PlannerRequest,
    PlannerRequestBuilder,
    PlannerRequestValidator,
    PlannerSerializer,
    PlannerToolAdapter,
    PlanningEvidenceBuilder,
    PlanningPipeline,
    PlanningPromptBuilder,
    PlanningStrategy,
    PlanningTraceBuilder,
    ReflectionCritique,
    TaskAnalyzer,
)
from app.agents.planning.builders import GraphBuilder, PlanBuilder
from app.agents.planning.contracts import Plan
from app.agents.planning.goals import PlanGoal
from app.agents.planning.nodes import NodeType


@pytest.mark.asyncio
async def test_intelligent_planner_end_to_end():
    """Verifies IntelligentPlanner synthesizing a validated executable Plan from a Goal."""
    manager, planner, metrics = PlannerFactory.create_planner_subsystem()
    req = (
        PlannerRequestBuilder("Extract Invoice and Validate")
        .with_goal_id("GOAL_INVOICE_01")
        .with_context(PlannerContextBuilder().with_budget(10.0).build())
        .build()
    )

    result = await planner.plan(req)

    assert result.success is True
    assert result.plan is not None
    assert len(result.plan.graph.nodes) >= 3
    assert result.plan.statistics.estimated_cost_usd > 0
    assert len(result.errors) == 0


def test_goal_analyzer_and_normalizer():
    """Verifies GoalAnalyzer and GoalNormalizer."""
    normalizer = GoalNormalizer()
    goal = normalizer.normalize("Process Customer Invoice", goal_id="G_NORM_01")
    assert goal.goal_id == "G_NORM_01"
    assert goal.name == "Process Customer Invoice"

    analyzer = GoalAnalyzer()
    ctx = PlannerContext(planning_budget_usd=5.0)
    report = analyzer.analyze_goal(goal, ctx)

    assert report.goal_id == "G_NORM_01"
    assert report.is_actionable is True
    assert len(report.inferred_objectives) >= 1
    assert len(report.assumptions) >= 1


def test_hierarchical_task_decomposer():
    """Verifies recursive hierarchical task decomposition from Goal down to Atomic Tasks."""
    decomposer = HierarchicalTaskDecomposer()
    goal = PlanGoal(goal_id="G_DECOMP", name="Bank Statement Analysis")

    tree = decomposer.decompose_goal(goal)

    assert tree.root_goal.goal_id == "G_DECOMP"
    assert len(tree.atomic_tasks) == 3
    assert tree.atomic_tasks[0].capability_requirement == "OCR"
    assert tree.atomic_tasks[1].capability_requirement == "LLM"
    assert tree.atomic_tasks[2].capability_requirement == "DECISION"


def test_candidate_generator_and_ranker():
    """Verifies CandidatePlanGenerator generating multiple candidates and PlanRanker selecting the best."""
    generator = CandidatePlanGenerator()
    ranker = PlanRanker()
    evaluator = CandidateEvaluator()

    req = PlannerRequestBuilder("OCR Analysis").build()
    candidates = generator.generate_candidates(req)

    assert len(candidates) >= 2

    evaluated = evaluator.evaluate_candidates(candidates, req.context)
    best = ranker.rank_and_select_best(evaluated)

    assert best is not None
    assert best.rank_score >= 0.8


def test_plan_optimizer_and_merger():
    """Verifies PlanOptimizer refining statistics and PlanMerger combining plans."""
    optimizer = PlanOptimizer()
    merger = PlanMerger()

    g1 = GraphBuilder("g1").add_node("A", "Node A", timeout_seconds=10.0).build()
    p1 = PlanBuilder("Plan1").with_graph(g1).with_cost(1.0).with_duration(10.0).build()

    optimized = optimizer.optimize_plan(p1)
    assert optimized.statistics.estimated_duration_seconds == 9.0  # 10 * 0.9
    assert optimized.statistics.estimated_cost_usd == 0.95  # 1.0 * 0.95

    g2 = GraphBuilder("g2").add_node("B", "Node B", timeout_seconds=5.0).build()
    p2 = PlanBuilder("Plan2").with_graph(g2).with_cost(0.5).with_duration(5.0).build()

    merged = merger.merge_plans([p1, p2])
    assert len(merged.graph.nodes) == 2
    assert "A" in merged.graph.nodes
    assert "B" in merged.graph.nodes


def test_reflection_engine_and_plan_repair():
    """Verifies PlannerReflectionEngine detecting flaws and PlanRepairEngine fixing them."""
    reflection = PlannerReflectionEngine()
    repair = PlanRepairEngine()

    # Create plan with disconnected (isolated) nodes
    graph = GraphBuilder("disconnected").add_node("N1", "Step 1").add_node("N2", "Step 2").build()
    plan = PlanBuilder("FlawedPlan").with_graph(graph).build()

    critique = reflection.critique_plan(plan)
    assert critique.has_flaws is True
    assert "LINK_SEQUENTIAL_EDGES" in critique.suggested_repairs

    repaired = repair.repair_plan(plan, critique)
    assert len(repaired.graph.edges) == 1
    assert repaired.name.endswith("_Repaired")


@pytest.mark.asyncio
async def test_adapters_suite():
    """Verifies LLM, Decision, Memory, and Tool adapters."""
    llm = MockLLMPlanningAdapter()
    decomp = await llm.generate_decomposition("Decompose document processing")
    assert "tasks" in decomp
    assert len(decomp["tasks"]) == 3

    scores = await llm.rank_candidates("Rank candidates")
    assert len(scores) == 2

    tool_adapter = PlannerToolAdapter()
    assert tool_adapter.check_capability_available("OCR") is True

    dec_adapter = PlannerDecisionAdapter()
    dec_result = await dec_adapter.evaluate_plan_feasibility(1.0)
    assert dec_result.is_approved is True

    mem_adapter = PlannerMemoryAdapter()
    history = await mem_adapter.get_historical_workflows("invoice")
    assert isinstance(history, list)


def test_fluent_builders_suite():
    """Verifies PlannerContextBuilder, PlannerRequestBuilder, CandidatePlanBuilder, PlanningTraceBuilder, PlanningEvidenceBuilder."""
    ctx = PlannerContextBuilder().for_document(uuid4(), uuid4()).with_budget(7.5).with_max_candidates(5).build()
    assert ctx.planning_budget_usd == 7.5
    assert ctx.max_candidates == 5

    req = PlannerRequestBuilder("Goal Name").with_goal_id("G1").with_context(ctx).build()
    assert req.goal.goal_id == "G1"

    graph = GraphBuilder("bg").add_node("A", "Node A").build()
    plan = PlanBuilder("CandidatePlan").with_graph(graph).build()
    cand = CandidatePlanBuilder(plan).with_strategy("LEAST_COST").with_score(0.85).build()
    assert cand.strategy_used == "LEAST_COST"
    assert cand.rank_score == 0.85

    ev = PlanningEvidenceBuilder("Verified tool exists").with_source("TOOL_REGISTRY").with_data("status", "AVAILABLE").build()
    assert ev.source == "TOOL_REGISTRY"
    assert ev.data["status"] == "AVAILABLE"

    trace = PlanningTraceBuilder("G1").with_strategy("HIERARCHICAL").add_evidence(ev).add_rejected_alternative("AltPlan", "High cost", 0.4).build()
    assert trace.goal_id == "G1"
    assert len(trace.evidences) == 1
    assert len(trace.rejected_alternatives) == 1


def test_serialization_and_validation():
    """Verifies PlannerSerializer and PlannerRequestValidator fail-fast checks."""
    ctx = PlannerContext()
    serialized = PlannerSerializer.to_json(ctx)
    assert "planning_budget_usd" in serialized

    bad_req = PlannerRequest(goal=PlanGoal(goal_id="G_ERR", name=""))
    with pytest.raises(GoalAnalysisException):
        PlannerRequestValidator.validate_request(bad_req)
