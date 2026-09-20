"""
Pattern Detector.
Identifies recurring patterns, systemic tool degradation, planner drift, and recovery hotspots
across multiple execution traces.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class DetectedPattern(BaseModel):
    """Represents a recurring behavioral or operational pattern detected across runs."""
    pattern_type: str  # RECURRING_FAILURE, RECURRING_SUCCESS, TOOL_DEGRADATION, PLANNER_DRIFT, RECOVERY_HOTSPOT
    description: str
    frequency: int = 1
    confidence: float = 0.9
    evidence: List[str] = Field(default_factory=list)
    remediation_hint: str = ""

    model_config = {"frozen": True}


class PatternDetector:
    """Detects cross-execution recurring phenomena and operational drifts."""

    def detect_patterns(
        self,
        current_trace: ExecutionTraceEnvelope,
        historical_traces: List[ExecutionTraceEnvelope]
    ) -> List[DetectedPattern]:
        """Analyzes current and historical traces to find trends and repeating patterns."""
        patterns: List[DetectedPattern] = []
        all_traces = [*historical_traces, current_trace]

        # 1. Recurring failures
        failed_tasks: Dict[str, int] = {}
        for tr in all_traces:
            for t in tr.tasks:
                if t.status == "FAILED" or t.error_message:
                    failed_tasks[t.task_name] = failed_tasks.get(t.task_name, 0) + 1

        for task_name, count in failed_tasks.items():
            if count >= 2:
                patterns.append(DetectedPattern(
                    pattern_type="RECURRING_FAILURE",
                    description=f"Task '{task_name}' failed across {count} executions.",
                    frequency=count,
                    confidence=0.95,
                    evidence=[f"Failed in {count}/{len(all_traces)} traces."],
                    remediation_hint=f"Review parameter schema and error handling for task '{task_name}'."
                ))

        # 2. Tool degradation
        tool_failures: Dict[str, int] = {}
        for tr in all_traces:
            for c in tr.tool_calls:
                if not c.success:
                    tool_failures[c.tool_name] = tool_failures.get(c.tool_name, 0) + 1

        for tool_name, failures in tool_failures.items():
            if failures >= 2:
                patterns.append(DetectedPattern(
                    pattern_type="TOOL_DEGRADATION",
                    description=f"Tool '{tool_name}' exhibited repeated failures ({failures} times).",
                    frequency=failures,
                    confidence=0.9,
                    evidence=[f"{failures} tool call failures recorded."],
                    remediation_hint=f"Enable circuit breaker or fallback tool for '{tool_name}'."
                ))

        # 3. Recurring success
        successful_traces = [tr for tr in all_traces if tr.final_state == "COMPLETED" and not tr.errors]
        if len(successful_traces) >= 2:
            patterns.append(DetectedPattern(
                pattern_type="RECURRING_SUCCESS",
                description=f"Stable goal completion observed in {len(successful_traces)} runs.",
                frequency=len(successful_traces),
                confidence=0.92,
                evidence=[f"{len(successful_traces)} flawless traces."],
                remediation_hint="Candidate for template decomposition promotion."
            ))

        return patterns
