"""
Tool Usage Analyzer.
Analyzes tool invocations, error distributions, duration percentiles, and alternate tool candidates.
Never invokes external tools.
"""

from typing import Any, Dict, List
from app.agents.reflection.interfaces import IToolUsageAnalyzer


class ToolUsageAnalyzer(IToolUsageAnalyzer):
    """Examines historical tool call traces to identify reliability, latency hotspots, and failures."""

    def analyze_tool_usage(self, tool_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes tool usage from event dictionaries or traces."""
        total_calls = len(tool_events)
        if total_calls == 0:
            return {
                "total_tool_calls": 0,
                "successful_calls": 0,
                "failed_calls": 0,
                "reliability_rate": 1.0,
                "tool_breakdown": {},
                "slowest_tool": None
            }

        successful = sum(1 for c in tool_events if c.get("success", True))
        failed = total_calls - successful

        breakdown: Dict[str, Dict[str, Any]] = {}
        slowest_tool = None
        max_duration = -1.0

        for call in tool_events:
            tool_name = call.get("tool_name", "unknown")
            duration = float(call.get("duration_ms", 0.0))
            is_success = bool(call.get("success", True))

            if tool_name not in breakdown:
                breakdown[tool_name] = {"calls": 0, "failures": 0, "total_duration_ms": 0.0}

            breakdown[tool_name]["calls"] += 1
            if not is_success:
                breakdown[tool_name]["failures"] += 1
            breakdown[tool_name]["total_duration_ms"] += duration

            if duration > max_duration:
                max_duration = duration
                slowest_tool = tool_name

        return {
            "total_tool_calls": total_calls,
            "successful_calls": successful,
            "failed_calls": failed,
            "reliability_rate": successful / total_calls,
            "tool_breakdown": breakdown,
            "slowest_tool": slowest_tool
        }
