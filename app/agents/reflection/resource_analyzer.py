"""
Resource Analyzer.
Evaluates memory, compute, token budget utilization, and dollar cost efficiency.
"""

from typing import Any, Dict
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class ResourceAnalyzer:
    """Analyzes resource consumption from trace metadata and execution telemetry."""

    def analyze_resources(self, trace: ExecutionTraceEnvelope) -> Dict[str, Any]:
        """Calculates token usage, financial cost, and worker resource utilization."""
        prompt_tokens = trace.token_usage.get("prompt_tokens", 0)
        completion_tokens = trace.token_usage.get("completion_tokens", 0)
        total_tokens = prompt_tokens + completion_tokens

        cost_usd = trace.cost_usd
        task_count = len(trace.tasks)
        avg_tokens_per_task = total_tokens / task_count if task_count > 0 else 0.0

        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost_usd,
            "average_tokens_per_task": avg_tokens_per_task,
            "is_cost_efficient": cost_usd < 1.0  # Threshold
        }
