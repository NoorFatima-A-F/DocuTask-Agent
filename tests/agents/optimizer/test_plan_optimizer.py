"""
Production Tests for Plan Optimization Engine.
Covers CostOptimizer, LatencyOptimizer, RiskOptimizer, OptimizationStrategy, and PlanSelector.
"""

import pytest

from app.agents.planning.execution_plan import ExecutionPlan, PlannedTask
from app.agents.planning.optimizer.cost_optimizer import CostOptimizer
from app.agents.planning.optimizer.latency_optimizer import LatencyOptimizer
from app.agents.planning.optimizer.optimization_strategy import (
    OptimizationStrategy,
    STRATEGY_PRESETS,
    StrategyWeights,
)
from app.agents.planning.optimizer.plan_selector import PlanEvaluationMetrics, PlanSelector
from app.agents.planning.optimizer.risk_optimizer import RiskOptimizer


@pytest.fixture
def sample_execution_plan() -> ExecutionPlan:
    plan = ExecutionPlan(
        plan_id="plan-opt-1",
        goal_id="goal-1",
        tasks=[
            PlannedTask(
                task_id="t_ocr",
                name="Ingest and OCR",
                action="ocr_document",
                required_tools=["gemini_vision"],
                dependencies=[],
                metadata={"is_digital_pdf": True},
                is_critical=True,
            ),
            PlannedTask(
                task_id="t_extract",
                name="Extract Fields",
                action="extract_fields",
                required_tools=["gemini_vision"],
                dependencies=["t_ocr"],
                is_critical=True,
            ),
            PlannedTask(
                task_id="t_val1",
                name="Validate Rule 1",
                action="validate_data",
                assigned_agent="ValidatorA",
                required_tools=["rule_validator"],
                dependencies=["t_extract"],
                is_critical=False,
            ),
            PlannedTask(
                task_id="t_val2",
                name="Validate Rule 2 (Duplicate)",
                action="validate_data",
                assigned_agent="ValidatorA",
                required_tools=["rule_validator"],
                dependencies=["t_extract"],
                is_critical=False,
            ),
        ],
    )
    return plan


class TestOptimizationStrategy:
    def test_presets_validity(self):
        for strat, weights in STRATEGY_PRESETS.items():
            assert weights.validate() is True

    def test_custom_weights_validation(self):
        w_valid = StrategyWeights(0.2, 0.2, 0.2, 0.2, 0.2)
        assert w_valid.validate() is True
        w_invalid = StrategyWeights(0.5, 0.5, 0.5, 0.0, 0.0)
        assert w_invalid.validate() is False


class TestCostOptimizer:
    def test_estimate_plan_cost(self, sample_execution_plan):
        optimizer = CostOptimizer()
        cost = optimizer.estimate_plan_cost(sample_execution_plan)
        assert cost > 0.0

    def test_cost_optimization_substitution_and_pruning(self, sample_execution_plan):
        optimizer = CostOptimizer()
        optimized_plan, savings = optimizer.optimize(sample_execution_plan)

        # gemini_vision on digital pdf should be replaced by pdf_plumber
        ocr_task = next(t for t in optimized_plan.tasks if t.task_id == "t_ocr")
        assert "pdf_plumber" in ocr_task.required_tools

        # duplicate non-critical validation should be pruned (4 tasks -> 3 tasks)
        assert len(optimized_plan.tasks) == 3
        assert savings > 0.0


class TestLatencyOptimizer:
    def test_compute_concurrency_waves(self, sample_execution_plan):
        optimizer = LatencyOptimizer()
        waves = optimizer.compute_concurrency_waves(sample_execution_plan)
        # Wave 0: t_ocr -> Wave 1: t_extract -> Wave 2: t_val1, t_val2
        assert len(waves) == 3
        assert len(waves[0]) == 1
        assert len(waves[2]) == 2

    def test_estimate_total_latency(self, sample_execution_plan):
        optimizer = LatencyOptimizer()
        latency = optimizer.estimate_total_latency(sample_execution_plan)
        assert latency > 0.0

    def test_latency_optimization_parallelization(self):
        plan = ExecutionPlan(
            plan_id="lat-plan",
            goal_id="goal-lat",
            tasks=[
                PlannedTask(task_id="t_ocr", name="OCR", action="ocr", dependencies=[]),
                PlannedTask(task_id="t_ext1", name="Ext 1", action="extract_header", dependencies=["t_ocr"]),
                PlannedTask(task_id="t_ext2", name="Ext 2", action="extract_tables", dependencies=["t_ocr", "t_ext1"]),
            ],
        )
        optimizer = LatencyOptimizer()
        opt_plan, speedup = optimizer.optimize(plan)
        ext2 = next(t for t in opt_plan.tasks if t.task_id == "t_ext2")
        # Chained extraction dependency should be parallelized to only depend on t_ocr
        assert ext2.dependencies == ["t_ocr"]
        assert speedup >= 0.0


class TestRiskOptimizer:
    def test_estimate_plan_risk(self, sample_execution_plan):
        optimizer = RiskOptimizer()
        risk = optimizer.estimate_plan_risk(sample_execution_plan)
        assert 0.0 <= risk <= 1.0

    def test_risk_optimization_injection(self, sample_execution_plan):
        optimizer = RiskOptimizer()
        hardened_plan, reduction = optimizer.optimize(sample_execution_plan)

        # Fallback strategies should be injected for critical tasks
        assert len(hardened_plan.fallback_strategies) >= 1
        # Extraction validation gate should be injected
        assert any(t.task_id.startswith("val_") for t in hardened_plan.tasks)
        assert reduction >= 0.0


class TestPlanSelector:
    def test_score_plan(self, sample_execution_plan):
        selector = PlanSelector()
        weights = STRATEGY_PRESETS[OptimizationStrategy.BALANCED]
        metrics = selector.score_plan(sample_execution_plan, "TestPlan", weights)

        assert isinstance(metrics, PlanEvaluationMetrics)
        assert 0.0 <= metrics.composite_score <= 1.0
        assert metrics.quality_score > 0.0
        assert metrics.cost_usd > 0.0
        assert metrics.latency_ms > 0.0

    def test_optimize_and_select_balanced(self, sample_execution_plan):
        selector = PlanSelector()
        result = selector.optimize_and_select(sample_execution_plan, OptimizationStrategy.BALANCED)

        assert result.selected_plan is not None
        assert result.winning_strategy == "balanced"
        assert result.winning_metrics.composite_score > 0.0
        assert len(result.all_evaluated_metrics) >= 4

    def test_optimize_and_select_cost_optimized(self, sample_execution_plan):
        selector = PlanSelector()
        result = selector.optimize_and_select(sample_execution_plan, OptimizationStrategy.COST_OPTIMIZED)
        assert result.winning_strategy == "cost_optimized"

    def test_optimize_and_select_latency_optimized(self, sample_execution_plan):
        selector = PlanSelector()
        result = selector.optimize_and_select(sample_execution_plan, OptimizationStrategy.LATENCY_OPTIMIZED)
        assert result.winning_strategy == "latency_optimized"

    def test_plan_evaluation_metrics_to_dict(self, sample_execution_plan):
        selector = PlanSelector()
        metrics = selector.score_plan(sample_execution_plan, "PlanA", STRATEGY_PRESETS[OptimizationStrategy.BALANCED])
        d = metrics.to_dict()
        assert d["plan_name"] == "PlanA"
        assert "composite_score" in d
        assert "quality_score" in d
        assert "latency_ms" in d

    @pytest.mark.parametrize(
        "strategy,expected_winner",
        [
            (OptimizationStrategy.BALANCED, "balanced"),
            (OptimizationStrategy.COST_OPTIMIZED, "cost_optimized"),
            (OptimizationStrategy.LATENCY_OPTIMIZED, "latency_optimized"),
            (OptimizationStrategy.RISK_MINIMIZED, "risk_minimized"),
            (OptimizationStrategy.QUALITY_OPTIMIZED, "quality_optimized"),
        ],
    )
    def test_all_strategy_presets_selection(self, sample_execution_plan, strategy, expected_winner):
        selector = PlanSelector()
        res = selector.optimize_and_select(sample_execution_plan, strategy)
        assert res.winning_strategy == expected_winner
        assert res.selected_plan is not None
        assert res.winning_metrics.composite_score > 0.0

    def test_latency_optimizer_diamond_dag(self):
        # A -> B, C -> D (Diamond)
        plan = ExecutionPlan(
            plan_id="diamond-plan",
            goal_id="g-diamond",
            tasks=[
                PlannedTask(task_id="A", name="Start", action="start", dependencies=[]),
                PlannedTask(task_id="B", name="Branch 1", action="process_1", dependencies=["A"]),
                PlannedTask(task_id="C", name="Branch 2", action="process_2", dependencies=["A"]),
                PlannedTask(task_id="D", name="Join", action="combine", dependencies=["B", "C"]),
            ],
        )
        optimizer = LatencyOptimizer()
        waves = optimizer.compute_concurrency_waves(plan)
        assert len(waves) == 3
        wave_ids = [[t.task_id for t in w] for w in waves]
        assert wave_ids[0] == ["A"]
        assert set(wave_ids[1]) == {"B", "C"}
        assert wave_ids[2] == ["D"]

    def test_latency_optimizer_single_and_empty_plan(self):
        optimizer = LatencyOptimizer()
        empty_plan = ExecutionPlan(plan_id="empty", goal_id="g", tasks=[])
        assert optimizer.compute_concurrency_waves(empty_plan) == []
        assert optimizer.estimate_total_latency(empty_plan) == 0.0

        single_plan = ExecutionPlan(
            plan_id="single",
            goal_id="g",
            tasks=[PlannedTask(task_id="t1", name="Only", action="act", dependencies=[])],
        )
        waves = optimizer.compute_concurrency_waves(single_plan)
        assert len(waves) == 1
        assert waves[0][0].task_id == "t1"
        assert optimizer.estimate_total_latency(single_plan) > 0.0

    def test_cost_optimizer_no_substitution_when_scanned(self):
        plan = ExecutionPlan(
            plan_id="scanned-plan",
            goal_id="g-scanned",
            tasks=[
                PlannedTask(
                    task_id="ocr_scan",
                    name="OCR Scanned Image",
                    action="ocr",
                    required_tools=["gemini_vision"],
                    dependencies=[],
                    metadata={"is_digital_pdf": False},
                )
            ],
        )
        optimizer = CostOptimizer()
        opt_plan, savings = optimizer.optimize(plan)
        # Should NOT substitute pdf_plumber for scanned document
        assert "gemini_vision" in opt_plan.tasks[0].required_tools
        assert savings == 0.0

    def test_risk_optimizer_all_critical_vs_none_critical(self):
        optimizer = RiskOptimizer()
        plan_none_crit = ExecutionPlan(
            plan_id="none-crit",
            goal_id="g",
            tasks=[
                PlannedTask(task_id="t1", name="T1", action="a1", dependencies=[], is_critical=False),
                PlannedTask(task_id="t2", name="T2", action="a2", dependencies=["t1"], is_critical=False),
            ],
        )
        risk_low = optimizer.estimate_plan_risk(plan_none_crit)

        plan_all_crit = ExecutionPlan(
            plan_id="all-crit",
            goal_id="g",
            tasks=[
                PlannedTask(task_id="t1", name="T1", action="a1", dependencies=[], is_critical=True),
                PlannedTask(task_id="t2", name="T2", action="a2", dependencies=["t1"], is_critical=True),
            ],
        )
        risk_high = optimizer.estimate_plan_risk(plan_all_crit)
        assert risk_high > risk_low

    def test_plan_selector_custom_extreme_weights(self, sample_execution_plan):
        selector = PlanSelector()
        # 100% cost sensitivity
        cost_weights = StrategyWeights(weight_quality=0.0, weight_cost=1.0, weight_latency=0.0, weight_reliability=0.0, weight_risk=0.0)
        res_cost = selector.score_plan(sample_execution_plan, "CostCentric", cost_weights)
        assert res_cost.composite_score > 0.0

        # 100% latency sensitivity
        lat_weights = StrategyWeights(weight_quality=0.0, weight_cost=0.0, weight_latency=1.0, weight_reliability=0.0, weight_risk=0.0)
        res_lat = selector.score_plan(sample_execution_plan, "LatencyCentric", lat_weights)
        assert res_lat.composite_score > 0.0

