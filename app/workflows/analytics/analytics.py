"""
Enterprise Workflow Analytics.
Aggregates execution metrics, latencies, failure rates, and AI token consumption.
"""

from typing import Any, Dict, List
from ..domain.models import ExecutionRecord, ExecutionState


class WorkflowAnalytics:
    """Calculates operational and business analytics over workflow execution histories."""

    @staticmethod
    def calculate_metrics(executions: List[ExecutionRecord]) -> Dict[str, Any]:
        """Aggregate execution statistics."""
        total = len(executions)
        if total == 0:
            return {
                "total_executions": 0,
                "success_rate": 100.0,
                "avg_duration_ms": 0.0,
                "failed_executions": 0,
            }

        completed = [e for e in executions if e.status == ExecutionState.COMPLETED]
        failed = [e for e in executions if e.status == ExecutionState.FAILED]

        durations = [e.duration_ms for e in completed if e.duration_ms > 0]
        avg_duration = sum(durations) / len(durations) if durations else 0.0
        success_rate = (len(completed) / total) * 100.0

        return {
            "total_executions": total,
            "completed_executions": len(completed),
            "failed_executions": len(failed),
            "success_rate": round(success_rate, 2),
            "avg_duration_ms": round(avg_duration, 2),
        }
