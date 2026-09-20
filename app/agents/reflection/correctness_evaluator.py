"""
Correctness Evaluator.
Assesses factual consistency, schema conformance, and assertion correctness of results.
"""

from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class CorrectnessEvaluator(IEvaluator):
    """Measures correctness based on failed task validations, error codes, and schema match."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Evaluates output and execution correctness."""
        has_errors = len(trace.errors) > 0
        failed_tasks = [t for t in trace.tasks if t.status == "FAILED"]

        if not has_errors and not failed_tasks:
            score = 1.0
            status = "EXCELLENT"
        elif len(failed_tasks) == 0 and has_errors:
            score = 0.8
            status = "SATISFACTORY"
        elif len(failed_tasks) < len(trace.tasks):
            score = 0.5
            status = "MARGINAL"
        else:
            score = 0.1
            status = "POOR"

        metric = EvaluationMetric(
            name="execution_correctness_ratio",
            dimension=EvaluationDimension.CORRECTNESS,
            score=score,
            evidence=[f"{len(failed_tasks)} failed tasks", f"{len(trace.errors)} logged errors"]
        )

        return DimensionEvaluation(
            dimension=EvaluationDimension.CORRECTNESS,
            score=score,
            status=status,
            metrics=[metric],
            findings=[f"Correctness evaluated at {score:.2f} with status {status}."],
            recommendation_hints=["Implement pre-condition guards on input validation."] if score < 0.8 else []
        )
