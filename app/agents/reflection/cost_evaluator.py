"""
Cost Evaluator.
Calculates and grades monetary expenditure against budget limits and baseline expectations.
"""

from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class CostEvaluator(IEvaluator):
    """Evaluates dollar cost of LLM model calls and infrastructure execution."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Evaluates cost efficiency."""
        cost = trace.cost_usd

        # Cost thresholds: < $0.05 is EXCELLENT (1.0), < $0.20 is SATISFACTORY (0.8), < $1.0 is MARGINAL (0.5), > $1.0 is POOR (0.2)
        if cost < 0.05:
            score = 1.0
            status = "EXCELLENT"
        elif cost < 0.20:
            score = 0.85
            status = "SATISFACTORY"
        elif cost < 1.0:
            score = 0.60
            status = "MARGINAL"
        else:
            score = max(0.1, 1.0 - (cost / 5.0))
            status = "POOR"

        metric = EvaluationMetric(
            name="monetary_cost_usd",
            dimension=EvaluationDimension.COST,
            score=score,
            evidence=[f"Actual cost: ${cost:.4f} USD"],
            details={"cost_usd": cost}
        )

        return DimensionEvaluation(
            dimension=EvaluationDimension.COST,
            score=score,
            status=status,
            metrics=[metric],
            findings=[f"Cost evaluated at ${cost:.4f} USD ({status})."],
            recommendation_hints=["Recommend prompt distillation or smaller model tier."] if score < 0.7 else []
        )
