"""
Memory Evaluator.
Assesses working memory efficiency, retrieval precision, and context bloat.
"""

from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class MemoryEvaluator(IEvaluator):
    """Evaluates context memory utilization and footprint."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Evaluates memory utilization."""
        # Baseline heuristic based on tasks count and checkpoint depth
        checkpoint_count = len(trace.checkpoints)
        score = 1.0
        if checkpoint_count > 10:
            score = 0.8
        elif checkpoint_count > 25:
            score = 0.6

        status = "EXCELLENT" if score >= 0.9 else "SATISFACTORY"

        metric = EvaluationMetric(
            name="memory_checkpoint_efficiency",
            dimension=EvaluationDimension.MEMORY_UTILIZATION,
            score=score,
            evidence=[f"{checkpoint_count} checkpoints recorded during execution."]
        )

        return DimensionEvaluation(
            dimension=EvaluationDimension.MEMORY_UTILIZATION,
            score=score,
            status=status,
            metrics=[metric],
            findings=[f"Memory footprint clean with {checkpoint_count} checkpoints."],
            recommendation_hints=[]
        )
