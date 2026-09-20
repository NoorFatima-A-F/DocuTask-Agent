"""
Confidence Evaluator.
Assesses model confidence calibration and reasoning certainty across decisions and tasks.
"""

from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class ConfidenceEvaluator(IEvaluator):
    """Evaluates the confidence calibration of reasoning steps and planner predictions."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Calculates confidence score distribution and calibration."""
        reasoning_steps = trace.reasoning_steps
        if not reasoning_steps:
            score = 0.8
            status = "SATISFACTORY"
            metrics = [EvaluationMetric(
                name="default_confidence",
                dimension=EvaluationDimension.CONFIDENCE,
                score=score,
                evidence=["No explicit reasoning steps provided; baseline confidence assumed."]
            )]
        else:
            scores = [step.confidence_score for step in reasoning_steps]
            score = sum(scores) / len(scores)
            status = "EXCELLENT" if score >= 0.85 else ("SATISFACTORY" if score >= 0.65 else "MARGINAL")
            metrics = [EvaluationMetric(
                name="reasoning_confidence_mean",
                dimension=EvaluationDimension.CONFIDENCE,
                score=score,
                evidence=[f"Evaluated {len(scores)} reasoning steps."]
            )]

        return DimensionEvaluation(
            dimension=EvaluationDimension.CONFIDENCE,
            score=score,
            status=status,
            metrics=metrics,
            findings=[f"Reasoning confidence calibrated at {score:.2f}."],
            recommendation_hints=["Require higher evidence threshold for low-confidence inferences."] if score < 0.7 else []
        )
