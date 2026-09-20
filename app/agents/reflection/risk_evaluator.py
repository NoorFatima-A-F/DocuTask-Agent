"""
Risk Evaluator.
Performs post-execution governance and safety audit across executed actions, tool calls, and decisions.
"""

from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class RiskEvaluator(IEvaluator):
    """Evaluates security, policy risk, and safety compliance across execution traces."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Evaluates governance and risk score."""
        decisions = trace.decisions
        if not decisions:
            score = 1.0
            status = "EXCELLENT"
            findings = ["No policy risk events triggered; clean execution."]
            metrics = [EvaluationMetric(
                name="policy_risk_score",
                dimension=EvaluationDimension.RISK_AND_SAFETY,
                score=1.0,
                evidence=["Zero high-risk decisions recorded."]
            )]
        else:
            risk_scores = [d.risk_score for d in decisions]
            avg_risk = sum(risk_scores) / len(risk_scores)
            # Invert risk: higher score = lower risk / safer
            safety_score = max(0.0, 1.0 - avg_risk)
            status = "EXCELLENT" if safety_score >= 0.9 else ("SATISFACTORY" if safety_score >= 0.7 else "POOR")
            metrics = [EvaluationMetric(
                name="policy_risk_score",
                dimension=EvaluationDimension.RISK_AND_SAFETY,
                score=safety_score,
                evidence=[f"Average decision risk level: {avg_risk:.3f}"]
            )]
            findings = [f"Safety rating: {status} with aggregate safety score {safety_score:.2f}."]

        return DimensionEvaluation(
            dimension=EvaluationDimension.RISK_AND_SAFETY,
            score=metrics[0].score,
            status=status,
            metrics=metrics,
            findings=findings,
            recommendation_hints=["Require human authorization for decisions with risk > 0.5."] if metrics[0].score < 0.7 else []
        )
