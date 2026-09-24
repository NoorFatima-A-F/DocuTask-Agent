"""
Reflection Root Cause Analyzer.
Performs post-mortem causal attribution for observed execution failures and inefficiencies.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class SystemicRootCause(BaseModel):
    """Diagnosed systemic reason for execution failure or degradation."""
    root_cause_id: str
    primary_fault_domain: str  # PLANNER, TOOL, INFRASTRUCTURE, POLICY, TIMEOUT
    description: str
    causal_factors: List[str] = Field(default_factory=list)
    confidence: float = 0.9
    preventative_action: str = ""

    model_config = {"frozen": True}


class ReflectionRootCauseAnalyzer:
    """Analyzes execution traces to isolate root causes without modifying runtime state."""

    def analyze_root_cause(self, trace: ExecutionTraceEnvelope) -> Optional[SystemicRootCause]:
        """Pinpoints the root cause of execution degradation or failure."""
        if trace.final_state == "COMPLETED" and not trace.errors:
            return None

        # Check for tool errors
        failed_tools = [c for c in trace.tool_calls if not c.success]
        if failed_tools:
            return SystemicRootCause(
                root_cause_id="TOOL_DOWNSTREAM_FAILURE",
                primary_fault_domain="TOOL",
                description=f"Downstream failure in tool '{failed_tools[0].tool_name}': {failed_tools[0].error_details}",
                causal_factors=[f"Tool {c.tool_name} failed" for c in failed_tools],
                confidence=0.95,
                preventative_action="Configure circuit breaker and secondary tool fallback."
            )

        # Check for timeouts
        if any("timeout" in err.lower() for err in trace.errors):
            return SystemicRootCause(
                root_cause_id="EXECUTION_TIMEOUT",
                primary_fault_domain="INFRASTRUCTURE",
                description="Task exceeded maximum allowed wall-clock duration.",
                causal_factors=trace.errors,
                confidence=0.90,
                preventative_action="Increase step timeout limit or partition task into smaller subtasks."
            )

        # Check for policy rejections
        denied_decisions = [d for d in trace.decisions if d.outcome != "ALLOWED"]
        if denied_decisions:
            return SystemicRootCause(
                root_cause_id="POLICY_REJECTION",
                primary_fault_domain="POLICY",
                description=f"Execution halted due to policy rule: {denied_decisions[0].policy_name}",
                causal_factors=[d.policy_name for d in denied_decisions],
                confidence=0.98,
                preventative_action="Refine plan preconditions to respect policy constraints."
            )

        return SystemicRootCause(
            root_cause_id="GENERIC_INTERNAL_ERROR",
            primary_fault_domain="PLANNER",
            description="Execution terminated with unhandled task errors.",
            causal_factors=trace.errors or ["Task state incomplete"],
            confidence=0.75,
            preventative_action="Enforce strict plan validation prior to dispatch."
        )
