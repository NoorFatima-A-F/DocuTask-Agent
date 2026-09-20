"""
Success Analyzer.
Analyzes patterns and factors that contributed to successful execution outcomes.
"""

from typing import Any, Dict
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class SuccessAnalyzer:
    """Identifies successful execution attributes to promote optimal planning and execution patterns."""

    def analyze_success(self, trace: ExecutionTraceEnvelope) -> Dict[str, Any]:
        """Identifies key success factors and optimal paths."""
        is_success = trace.final_state == "COMPLETED"
        has_outputs = len(trace.final_outputs) > 0
        zero_retries = all(t.retry_count == 0 for t in trace.tasks)
        zero_recoveries = len(trace.recovery_actions) == 0

        flawless = is_success and zero_retries and zero_recoveries and len(trace.errors) == 0

        return {
            "is_success": is_success,
            "has_outputs": has_outputs,
            "zero_retries": zero_retries,
            "flawless_execution": flawless,
            "success_factor_count": sum([is_success, has_outputs, zero_retries, zero_recoveries])
        }
