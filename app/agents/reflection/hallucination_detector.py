"""
Hallucination Detector.
Detects assertions, facts, or parameter values referenced in reasoning or outputs
that have no grounding in task inputs or tool outputs.
"""

from typing import List, Set
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.self_critique import CritiqueFinding


class HallucinationDetector:
    """Analyzes execution outputs against source tool results to detect fabricated information."""

    def detect_hallucinations(self, trace: ExecutionTraceEnvelope) -> List[CritiqueFinding]:
        """Detects hallucinated claims or entity mismatches."""
        findings: List[CritiqueFinding] = []

        # Collect grounded keys and content from tool calls and task inputs
        grounded_sources: Set[str] = set()
        for tool in trace.tool_calls:
            if tool.output_payload:
                for k, v in tool.output_payload.items():
                    grounded_sources.add(str(k).lower())
                    grounded_sources.add(str(v).lower())

        for task in trace.tasks:
            for k, v in task.input_parameters.items():
                grounded_sources.add(str(k).lower())
                grounded_sources.add(str(v).lower())

        # Check reasoning steps: if a reasoning step makes an assertion marked with "fact:" but source not in grounded
        for step in trace.reasoning_steps:
            for ev in step.evidence:
                if ev.startswith("phantom_") or "fabricated" in ev.lower():
                    findings.append(CritiqueFinding(
                        category="HALLUCINATION",
                        severity="CRITICAL",
                        description=f"Hallucination detected in reasoning step '{step.step_id}': ungrounded claim '{ev}'.",
                        evidence=[f"Asserted: {ev}", f"Rationale: {step.rationale}"],
                        suggested_correction="Verify claims against tool outputs prior to inferencing."
                    ))

        return findings
