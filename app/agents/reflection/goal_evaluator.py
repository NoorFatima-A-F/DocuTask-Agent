"""
Goal Evaluator.
Assesses whether the original user goal was achieved, partially achieved, failed, or exceeded.
"""

from typing import Any, Dict
from app.agents.reflection.evaluation import DimensionEvaluation, EvaluationDimension, EvaluationMetric
from app.agents.reflection.interfaces import IEvaluator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class GoalEvaluator(IEvaluator):
    """Evaluates goal achievement based on final execution state, task completion, and outputs."""

    def evaluate(self, trace: ExecutionTraceEnvelope) -> DimensionEvaluation:
        """Evaluates goal success and returns a structured DimensionEvaluation."""
        total_tasks = len(trace.tasks)
        completed_tasks = sum(1 for t in trace.tasks if t.status == "COMPLETED")
        has_outputs = bool(trace.final_outputs)
        is_completed = trace.final_state == "COMPLETED"

        if is_completed and completed_tasks == total_tasks and has_outputs:
            score = 1.0
            status = "EXCEEDED" if trace.total_duration_ms < 5000 else "SATISFACTORY"
        elif is_completed and completed_tasks > 0:
            score = 0.8
            status = "SATISFACTORY"
        elif completed_tasks > 0:
            score = 0.5
            status = "PARTIALLY_ACHIEVED"
        else:
            score = 0.0
            status = "FAILED"

        metric = EvaluationMetric(
            name="goal_achievement_rate",
            dimension=EvaluationDimension.GOAL_ACHIEVEMENT,
            score=score,
            confidence=0.95,
            evidence=[f"State: {trace.final_state}", f"Completed {completed_tasks}/{total_tasks} tasks"],
            details={"has_outputs": has_outputs, "status": status}
        )

        return DimensionEvaluation(
            dimension=EvaluationDimension.GOAL_ACHIEVEMENT,
            score=score,
            status=status,
            metrics=[metric],
            findings=[f"Execution concluded with state {trace.final_state} and status {status}."],
            recommendation_hints=["Ensure all planned subtasks produce non-empty outputs."] if not has_outputs else []
        )
