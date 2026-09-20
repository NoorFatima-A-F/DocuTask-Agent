"""
Efficiency Evaluator.
Evaluates minimal required steps vs actual steps, retry overhead, and unnecessary execution paths.
"""

from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class EfficiencyEvaluator(IEvaluator):
    """Calculates execution path efficiency by comparing total tasks against redundant or retried tasks."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Evaluates efficiency."""
        total_tasks = len(trace.tasks)
        if total_tasks == 0:
            return DimensionEvaluation(
                dimension=EvaluationDimension.EFFICIENCY,
                score=1.0,
                status="EXCELLENT",
                findings=["Zero tasks in execution trace."]
            )

        retries = sum(t.retry_count for t in trace.tasks)
        efficiency_score = 1.0
        if retries > 0:
            efficiency_score -= min(0.4, retries * 0.1)
        if len(trace.recovery_actions) > 0:
            efficiency_score -= min(0.3, len(trace.recovery_actions) * 0.15)
        efficiency_score = max(0.1, efficiency_score)

        status = "EXCELLENT" if efficiency_score >= 0.9 else ("SATISFACTORY" if efficiency_score >= 0.7 else "MARGINAL")

        metric = EvaluationMetric(
            name="task_path_efficiency",
            dimension=EvaluationDimension.EFFICIENCY,
            score=efficiency_score,
            evidence=[f"{retries} retries across {total_tasks} tasks."]
        )

        return DimensionEvaluation(
            dimension=EvaluationDimension.EFFICIENCY,
            score=efficiency_score,
            status=status,
            metrics=[metric],
            findings=[f"Workflow efficiency calculated at {efficiency_score:.2f}."],
            recommendation_hints=["Consider reducing retry thresholds on flaky tasks."] if efficiency_score < 0.8 else []
        )
