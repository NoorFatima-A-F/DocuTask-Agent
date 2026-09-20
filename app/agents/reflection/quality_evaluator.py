"""
Quality Evaluator.
Evaluates the qualitative standards of generated execution outputs and artifacts.
"""

from typing import Any
from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class QualityEvaluator(IEvaluator):
    """Computes output quality score based on structure, completeness, and error rates."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Evaluates execution quality."""
        error_count = len(trace.errors)
        output_count = len(trace.final_outputs)

        quality_score = 1.0
        if error_count > 0:
            quality_score -= min(0.5, error_count * 0.15)
        if output_count == 0 and trace.final_state == "COMPLETED":
            quality_score -= 0.3
        quality_score = max(0.0, min(1.0, quality_score))

        status = "EXCELLENT" if quality_score >= 0.9 else ("SATISFACTORY" if quality_score >= 0.7 else "POOR")

        metric = EvaluationMetric(
            name="output_quality_score",
            dimension=EvaluationDimension.QUALITY,
            score=quality_score,
            confidence=0.9,
            evidence=[f"Output fields count: {output_count}", f"Errors encountered: {error_count}"]
        )

        return DimensionEvaluation(
            dimension=EvaluationDimension.QUALITY,
            score=quality_score,
            status=status,
            metrics=[metric],
            findings=[f"Overall output quality rated {status} ({quality_score:.2f})."],
            recommendation_hints=["Enhance validation of generated intermediate fields."] if quality_score < 0.8 else []
        )
