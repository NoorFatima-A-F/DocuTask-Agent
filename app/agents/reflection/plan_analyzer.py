"""
Plan Analyzer.
Evaluates the quality of plan decomposition, redundant or duplicated tasks, missing dependencies,
and structural complexity.
"""

from typing import Any, Dict
from app.agents.reflection.interfaces import IPlanAnalyzer
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class PlanAnalyzer(IPlanAnalyzer):
    """Analyzes plan decomposition and structural efficiency without modifying or generating plans."""

    def analyze_plan(self, plan: Any, trace: ExecutionTraceEnvelope) -> Dict[str, Any]:
        """Examines tasks in trace for duplicates, granularity, and redundant execution paths."""
        task_names = [t.task_name.lower().strip() for t in trace.tasks]
        unique_names = set(task_names)
        duplicated_count = len(task_names) - len(unique_names)

        # Detect redundant/zero-effect tasks (tasks with duration < 1ms and no outputs)
        redundant_tasks = [
            t.task_name for t in trace.tasks
            if t.duration_ms < 1.0 and (not t.output_result or t.output_result == {})
        ]

        decomposition_score = 1.0
        if duplicated_count > 0:
            decomposition_score -= min(0.3, duplicated_count * 0.1)
        if len(redundant_tasks) > 0:
            decomposition_score -= min(0.3, len(redundant_tasks) * 0.1)
        decomposition_score = max(0.0, decomposition_score)

        return {
            "total_tasks_planned": len(trace.tasks),
            "unique_task_types": len(unique_names),
            "duplicated_task_count": duplicated_count,
            "redundant_tasks": redundant_tasks,
            "decomposition_efficiency_score": decomposition_score,
            "has_excessive_branching": len(trace.tasks) > 20
        }
