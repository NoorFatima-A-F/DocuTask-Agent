"""
Latency Evaluator.
Assesses total wall-clock duration and critical path delays against performance SLAs.
"""

from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class LatencyEvaluator(IEvaluator):
    """Evaluates wall-clock latency against expected execution SLO thresholds."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Evaluates latency performance."""
        duration_ms = trace.total_duration_ms

        # Thresholds: < 2000ms = 1.0 (EXCELLENT), < 10000ms = 0.85 (SATISFACTORY), < 30000ms = 0.6 (MARGINAL), else POOR
        if duration_ms < 2000.0:
            score = 1.0
            status = "EXCELLENT"
        elif duration_ms < 10000.0:
            score = 0.85
            status = "SATISFACTORY"
        elif duration_ms < 30000.0:
            score = 0.60
            status = "MARGINAL"
        else:
            score = max(0.1, 1.0 - (duration_ms / 60000.0))
            status = "POOR"

        metric = EvaluationMetric(
            name="wall_clock_latency_ms",
            dimension=EvaluationDimension.LATENCY,
            score=score,
            evidence=[f"Duration: {duration_ms:.1f}ms"],
            details={"duration_ms": duration_ms}
        )

        return DimensionEvaluation(
            dimension=EvaluationDimension.LATENCY,
            score=score,
            status=status,
            metrics=[metric],
            findings=[f"Execution took {duration_ms:.1f}ms ({status})."],
            recommendation_hints=["Enable parallel node execution for independent subtasks."] if score < 0.7 else []
        )
