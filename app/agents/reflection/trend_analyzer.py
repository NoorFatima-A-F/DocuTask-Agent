"""
Trend Analyzer.
Computes longitudinal trends for latency, token consumption, cost, and planner accuracy over time.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class TrendReport(BaseModel):
    """Longitudinal metrics trend summary."""
    latency_trend: str  # DECREASING, STABLE, INCREASING
    cost_trend: str  # DECREASING, STABLE, INCREASING
    token_trend: str  # DECREASING, STABLE, INCREASING
    sample_size: int = 1
    average_duration_ms: float = 0.0
    average_cost_usd: float = 0.0

    model_config = {"frozen": True}


class TrendAnalyzer:
    """Calculates temporal trajectories of agent execution parameters."""

    def analyze_trends(
        self,
        current_trace: ExecutionTraceEnvelope,
        historical_traces: List[ExecutionTraceEnvelope]
    ) -> TrendReport:
        """Determines if cost, latency, or tokens are drifting or improving."""
        all_traces = [*historical_traces, current_trace]
        count = len(all_traces)
        if count < 2:
            return TrendReport(
                latency_trend="STABLE",
                cost_trend="STABLE",
                token_trend="STABLE",
                sample_size=count,
                average_duration_ms=current_trace.total_duration_ms,
                average_cost_usd=current_trace.cost_usd
            )

        durations = [t.total_duration_ms for t in all_traces]
        costs = [t.cost_usd for t in all_traces]
        tokens = [t.token_usage.get("prompt_tokens", 0) + t.token_usage.get("completion_tokens", 0) for t in all_traces]

        def _trend(values: List[float]) -> str:
            if len(values) < 2:
                return "STABLE"
            diff = values[-1] - values[0]
            if abs(diff) < 0.05 * (values[0] or 1.0):
                return "STABLE"
            return "INCREASING" if diff > 0 else "DECREASING"

        return TrendReport(
            latency_trend=_trend(durations),
            cost_trend=_trend(costs),
            token_trend=_trend([float(v) for v in tokens]),
            sample_size=count,
            average_duration_ms=sum(durations) / count,
            average_cost_usd=sum(costs) / count
        )
