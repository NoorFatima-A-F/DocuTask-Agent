"""
Token Evaluator.
Analyzes prompt and completion token efficiency, context window utilization, and verbosity.
"""

from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class TokenEvaluator(IEvaluator):
    """Measures token consumption economy and context window optimization."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Evaluates token usage."""
        prompt = trace.token_usage.get("prompt_tokens", 0)
        completion = trace.token_usage.get("completion_tokens", 0)
        total = prompt + completion

        if total < 2000:
            score = 1.0
            status = "EXCELLENT"
        elif total < 8000:
            score = 0.85
            status = "SATISFACTORY"
        elif total < 32000:
            score = 0.65
            status = "MARGINAL"
        else:
            score = max(0.1, 1.0 - (total / 100000.0))
            status = "POOR"

        metric = EvaluationMetric(
            name="total_tokens_consumed",
            dimension=EvaluationDimension.TOKEN_UTILIZATION,
            score=score,
            evidence=[f"{total} tokens consumed ({prompt} prompt / {completion} completion)"],
            details={"prompt_tokens": prompt, "completion_tokens": completion, "total_tokens": total}
        )

        return DimensionEvaluation(
            dimension=EvaluationDimension.TOKEN_UTILIZATION,
            score=score,
            status=status,
            metrics=[metric],
            findings=[f"Total token footprint: {total} ({status})."],
            recommendation_hints=["Trim conversational history or inject summary contexts."] if score < 0.7 else []
        )
