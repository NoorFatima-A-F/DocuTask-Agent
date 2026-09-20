"""
Performance Analyzer.
Analyzes parallelism, critical path latency, worker scheduling delays, and idle time.
"""

from typing import Any, Dict
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class PerformanceAnalyzer:
    """Evaluates concurrency efficiency, latency bottlenecks, and idle time."""

    def analyze_performance(self, trace: ExecutionTraceEnvelope) -> Dict[str, Any]:
        """Calculates throughput, execution latency, and concurrency metrics."""
        total_duration = trace.total_duration_ms
        task_durations = [t.duration_ms for t in trace.tasks]
        sum_task_duration = sum(task_durations)

        # Theoretical parallelism factor = sum(task durations) / total execution duration
        parallelism_factor = (
            sum_task_duration / total_duration
            if total_duration > 0.0 else 1.0
        )

        return {
            "total_duration_ms": total_duration,
            "sum_task_duration_ms": sum_task_duration,
            "parallelism_factor": parallelism_factor,
            "is_parallelized": parallelism_factor > 1.1,
            "task_count": len(trace.tasks)
        }
