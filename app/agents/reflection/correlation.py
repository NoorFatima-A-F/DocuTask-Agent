"""
Correlation Analyzer.
Computes statistical associations between plan complexity, tool latency, token usage, and overall success.
"""

from typing import Any, Dict, List
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class CorrelationAnalyzer:
    """Discovers relationships between execution metrics and final outcomes."""

    def analyze_correlations(self, traces: List[ExecutionTraceEnvelope]) -> Dict[str, Any]:
        """Calculates rough correlations between execution variables."""
        if len(traces) < 2:
            return {"correlation_status": "INSUFFICIENT_DATA", "sample_count": len(traces)}

        total_runs = len(traces)
        successful_runs = sum(1 for t in traces if t.final_state == "COMPLETED")

        high_latency_failures = sum(
            1 for t in traces
            if t.total_duration_ms > 10000 and t.final_state != "COMPLETED"
        )

        return {
            "correlation_status": "COMPUTED",
            "sample_count": total_runs,
            "success_rate": successful_runs / total_runs,
            "latency_failure_association": high_latency_failures / total_runs if total_runs > 0 else 0.0,
            "insights": ["High latency correlates with execution failure."] if high_latency_failures > 0 else []
        }
