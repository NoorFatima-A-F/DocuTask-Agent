"""
Comparative Analysis Engine.
Compares a target execution run against historic baselines or alternative execution paths.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class ComparisonResult(BaseModel):
    """Structured delta between current execution and historical baseline."""
    execution_id: str
    baseline_id: Optional[str] = None
    duration_delta_ms: float = 0.0
    cost_delta_usd: float = 0.0
    token_delta: int = 0
    is_improvement: bool = True
    summary: str = ""

    model_config = {"frozen": True}


class ComparativeAnalyzer:
    """Compares current execution performance against historical baseline."""

    def compare_traces(
        self,
        current: ExecutionTraceEnvelope,
        baseline: Optional[ExecutionTraceEnvelope]
    ) -> ComparisonResult:
        """Computes comparative deltas against baseline."""
        if not baseline:
            return ComparisonResult(
                execution_id=str(current.execution_id),
                is_improvement=True,
                summary="Initial run, no baseline available for comparison."
            )

        duration_delta = current.total_duration_ms - baseline.total_duration_ms
        cost_delta = current.cost_usd - baseline.cost_usd
        curr_tokens = current.token_usage.get("prompt_tokens", 0) + current.token_usage.get("completion_tokens", 0)
        base_tokens = baseline.token_usage.get("prompt_tokens", 0) + baseline.token_usage.get("completion_tokens", 0)
        token_delta = curr_tokens - base_tokens

        is_improvement = (duration_delta <= 0) and (cost_delta <= 0) and (current.final_state == "COMPLETED")

        summary = (
            f"Run duration {'faster' if duration_delta <= 0 else 'slower'} by {abs(duration_delta):.1f}ms; "
            f"cost {'lower' if cost_delta <= 0 else 'higher'} by ${abs(cost_delta):.4f} USD."
        )

        return ComparisonResult(
            execution_id=str(current.execution_id),
            baseline_id=str(baseline.execution_id),
            duration_delta_ms=duration_delta,
            cost_delta_usd=cost_delta,
            token_delta=token_delta,
            is_improvement=is_improvement,
            summary=summary
        )
