"""
Bias Detector.
Detects tool preference skew, decision conservatism bias, and non-optimal route fixation.
"""

from typing import List
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.self_critique import CritiqueFinding


class BiasDetector:
    """Audits decision paths and tool selections for systemic bias or preference fixation."""

    def detect_bias(self, trace: ExecutionTraceEnvelope) -> List[CritiqueFinding]:
        """Examines tool call distributions and decision outcomes."""
        findings: List[CritiqueFinding] = []

        # Tool monopoly bias: 1 tool called >90% of times when >= 10 calls made
        tool_names = [t.tool_name for t in trace.tool_calls]
        if len(tool_names) >= 10:
            counts = {name: tool_names.count(name) for name in set(tool_names)}
            for tool, count in counts.items():
                if count / len(tool_names) >= 0.90 and len(set(tool_names)) > 1:
                    findings.append(CritiqueFinding(
                        category="BIAS",
                        severity="LOW",
                        description=f"Tool selection bias observed: tool '{tool}' represents {count/len(tool_names):.1%} of all calls.",
                        evidence=[f"Tool {tool} called {count}/{len(tool_names)} times."],
                        suggested_correction="Evaluate if specialized alternate tools provide superior efficiency."
                    ))

        return findings
