"""
Evaluation Pipeline.
Orchestrates execution of analyzers and dimension evaluators across an execution trace
to synthesize a comprehensive, strongly typed EvaluationReport.
"""

from typing import Dict, List, Optional
from uuid import uuid4
from app.agents.reflection.confidence_evaluator import ConfidenceEvaluator
from app.agents.reflection.correctness_evaluator import CorrectnessEvaluator
from app.agents.reflection.cost_evaluator import CostEvaluator
from app.agents.reflection.decision_analyzer import DecisionAnalyzer
from app.agents.reflection.efficiency_evaluator import EfficiencyEvaluator
from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationReport
from app.agents.reflection.execution_analyzer import ExecutionAnalyzer
from app.agents.reflection.failure_analyzer import FailureAnalyzer
from app.agents.reflection.goal_evaluator import GoalEvaluator
from app.agents.reflection.latency_evaluator import LatencyEvaluator
from app.agents.reflection.memory_evaluator import MemoryEvaluator
from app.agents.reflection.performance_analyzer import PerformanceAnalyzer
from app.agents.reflection.plan_analyzer import PlanAnalyzer
from app.agents.reflection.quality_evaluator import QualityEvaluator
from app.agents.reflection.reasoning_analyzer import ReasoningAnalyzer
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.resource_analyzer import ResourceAnalyzer
from app.agents.reflection.risk_evaluator import RiskEvaluator
from app.agents.reflection.success_analyzer import SuccessAnalyzer
from app.agents.reflection.token_evaluator import TokenEvaluator
from app.agents.reflection.tool_usage_analyzer import ToolUsageAnalyzer


class EvaluationPipeline:
    """End-to-end evaluation pipeline aggregating analyzers and dimensional evaluators."""

    def __init__(
        self,
        goal_evaluator: Optional[GoalEvaluator] = None,
        quality_evaluator: Optional[QualityEvaluator] = None,
        confidence_evaluator: Optional[ConfidenceEvaluator] = None,
        correctness_evaluator: Optional[CorrectnessEvaluator] = None,
        efficiency_evaluator: Optional[EfficiencyEvaluator] = None,
        cost_evaluator: Optional[CostEvaluator] = None,
        latency_evaluator: Optional[LatencyEvaluator] = None,
        token_evaluator: Optional[TokenEvaluator] = None,
        memory_evaluator: Optional[MemoryEvaluator] = None,
        risk_evaluator: Optional[RiskEvaluator] = None,
    ):
        self.goal_evaluator = goal_evaluator or GoalEvaluator()
        self.quality_evaluator = quality_evaluator or QualityEvaluator()
        self.confidence_evaluator = confidence_evaluator or ConfidenceEvaluator()
        self.correctness_evaluator = correctness_evaluator or CorrectnessEvaluator()
        self.efficiency_evaluator = efficiency_evaluator or EfficiencyEvaluator()
        self.cost_evaluator = cost_evaluator or CostEvaluator()
        self.latency_evaluator = latency_evaluator or LatencyEvaluator()
        self.token_evaluator = token_evaluator or TokenEvaluator()
        self.memory_evaluator = memory_evaluator or MemoryEvaluator()
        self.risk_evaluator = risk_evaluator or RiskEvaluator()

        self.execution_analyzer = ExecutionAnalyzer()
        self.plan_analyzer = PlanAnalyzer()
        self.reasoning_analyzer = ReasoningAnalyzer()
        self.decision_analyzer = DecisionAnalyzer()
        self.tool_analyzer = ToolUsageAnalyzer()
        self.resource_analyzer = ResourceAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.failure_analyzer = FailureAnalyzer()
        self.success_analyzer = SuccessAnalyzer()

    def run_pipeline(self, trace: ExecutionTraceEnvelope) -> EvaluationReport:
        """Executes all dimensional evaluations and returns an EvaluationReport."""
        dimensions: Dict[str, DimensionEvaluation] = {}

        # 1. Run dimensional evaluations
        evaluators = [
            (EvaluationDimension.GOAL_ACHIEVEMENT.value, self.goal_evaluator),
            (EvaluationDimension.QUALITY.value, self.quality_evaluator),
            (EvaluationDimension.CONFIDENCE.value, self.confidence_evaluator),
            (EvaluationDimension.CORRECTNESS.value, self.correctness_evaluator),
            (EvaluationDimension.EFFICIENCY.value, self.efficiency_evaluator),
            (EvaluationDimension.COST.value, self.cost_evaluator),
            (EvaluationDimension.LATENCY.value, self.latency_evaluator),
            (EvaluationDimension.TOKEN_UTILIZATION.value, self.token_evaluator),
            (EvaluationDimension.MEMORY_UTILIZATION.value, self.memory_evaluator),
            (EvaluationDimension.RISK_AND_SAFETY.value, self.risk_evaluator),
        ]

        scores: List[float] = []
        strengths: List[str] = []
        weaknesses: List[str] = []

        for dim_name, eval_inst in evaluators:
            res: DimensionEvaluation = eval_inst.evaluate(trace)
            dimensions[dim_name] = res
            scores.append(res.score)
            if res.score >= 0.85 and res.findings:
                strengths.append(f"[{dim_name}] {res.findings[0]}")
            elif res.score < 0.70 and res.findings:
                weaknesses.append(f"[{dim_name}] {res.findings[0]}")

        overall_score = sum(scores) / len(scores) if scores else 0.0

        summary = (
            f"Execution evaluated with overall score {overall_score:.2f}. "
            f"Goal status: {dimensions[EvaluationDimension.GOAL_ACHIEVEMENT.value].status}."
        )

        return EvaluationReport(
            report_id=uuid4(),
            execution_id=trace.execution_id,
            overall_score=overall_score,
            dimensions=dimensions,
            summary=summary,
            key_strengths=strengths,
            key_weaknesses=weaknesses
        )
