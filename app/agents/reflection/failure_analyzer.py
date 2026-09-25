"""
Failure Analyzer.
Investigates failed tasks, error logs, and recovery attempts in finished execution traces.
Does not perform recovery; only diagnoses reasons for failure.
"""

from typing import Any, Dict
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class FailureAnalyzer:
    """Diagnoses systemic or transient failures observed in completed execution traces."""

    def analyze_failures(self, trace: ExecutionTraceEnvelope) -> Dict[str, Any]:
        """Categorizes failure modes and assesses recovery impact."""
        failed_tasks = [t for t in trace.tasks if t.status == "FAILED" or t.error_message]
        errors = list(trace.errors)
        for t in failed_tasks:
            if t.error_message and t.error_message not in errors:
                errors.append(f"{t.task_name}: {t.error_message}")

        recovery_count = len(trace.recovery_actions)

        # Categorize common failure signatures
        categories: Dict[str, int] = {}
        for err in errors:
            err_lower = err.lower()
            if "timeout" in err_lower:
                categories["timeout"] = categories.get("timeout", 0) + 1
            elif "tool" in err_lower or "api" in err_lower:
                categories["tool_failure"] = categories.get("tool_failure", 0) + 1
            elif "permission" in err_lower or "auth" in err_lower:
                categories["auth_failure"] = categories.get("auth_failure", 0) + 1
            else:
                categories["internal_error"] = categories.get("internal_error", 0) + 1

        return {
            "has_failures": len(failed_tasks) > 0 or len(errors) > 0,
            "failed_task_count": len(failed_tasks),
            "total_errors": len(errors),
            "error_categories": categories,
            "recovery_attempts_observed": recovery_count,
            "recovered_successfully": trace.final_state == "COMPLETED" and recovery_count > 0
        }
