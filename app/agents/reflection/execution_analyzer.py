"""
Execution Analyzer.
Examines task execution traces, lifecycle transitions, retries, worker allocation, and bottlenecks.
"""

from typing import Any, Dict
from app.agents.reflection.interfaces import IExecutionAnalyzer
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class ExecutionAnalyzer(IExecutionAnalyzer):
    """Analyzes execution traces to compute task success rates, duration distributions, and retries."""

    def analyze_execution(self, trace: ExecutionTraceEnvelope) -> Dict[str, Any]:
        """Calculates runtime execution metrics from trace."""
        tasks = trace.tasks
        total_tasks = len(tasks)
        if total_tasks == 0:
            return {
                "total_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "retry_count": 0,
                "success_rate": 1.0 if trace.final_state == "COMPLETED" else 0.0,
                "average_task_duration_ms": 0.0,
                "bottleneck_task": None
            }

        completed = sum(1 for t in tasks if t.status == "COMPLETED")
        failed = sum(1 for t in tasks if t.status == "FAILED")
        retries = sum(t.retry_count for t in tasks)
        durations = [t.duration_ms for t in tasks]
        avg_dur = sum(durations) / total_tasks if durations else 0.0

        slowest_task = max(tasks, key=lambda t: t.duration_ms) if tasks else None

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed,
            "failed_tasks": failed,
            "retry_count": retries,
            "success_rate": completed / total_tasks,
            "average_task_duration_ms": avg_dur,
            "bottleneck_task": slowest_task.task_name if slowest_task else None,
            "total_duration_ms": trace.total_duration_ms
        }
