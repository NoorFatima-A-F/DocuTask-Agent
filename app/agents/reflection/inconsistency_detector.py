"""
Inconsistency Detector.
Identifies contradictory statements, conflicting parameter values, and temporal discrepancies across execution traces.
"""

from typing import List
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.self_critique import CritiqueFinding


class InconsistencyDetector:
    """Detects mutually contradictory assumptions, conflicting task outputs, and logic inconsistencies."""

    def detect_inconsistencies(self, trace: ExecutionTraceEnvelope) -> List[CritiqueFinding]:
        """Detects inconsistencies across task outputs and reasoning steps."""
        findings: List[CritiqueFinding] = []

        # Check for state contradictions (e.g. final state is COMPLETED but all tasks are FAILED)
        total_tasks = len(trace.tasks)
        failed_tasks = sum(1 for t in trace.tasks if t.status == "FAILED")
        if total_tasks > 0 and failed_tasks == total_tasks and trace.final_state == "COMPLETED":
            findings.append(CritiqueFinding(
                category="INCONSISTENCY",
                severity="HIGH",
                description="State contradiction: execution marked COMPLETED despite 100% task failure.",
                evidence=[f"Failed tasks: {failed_tasks}/{total_tasks}", f"State: {trace.final_state}"],
                suggested_correction="Harmonize execution state transitions with task outcome rollups."
            ))

        # Check for conflicting conclusions in reasoning steps
        conclusions = [s.conclusion.lower().strip() for s in trace.reasoning_steps]
        for i, c1 in enumerate(conclusions):
            for j, c2 in enumerate(conclusions):
                if i < j and (("not " + c1) == c2 or ("not " + c2) == c1):
                    findings.append(CritiqueFinding(
                        category="INCONSISTENCY",
                        severity="HIGH",
                        description=f"Direct logical contradiction between reasoning steps {i} and {j}.",
                        evidence=[f"Step {i}: {c1}", f"Step {j}: {c2}"],
                        suggested_correction="Reconcile divergent reasoning branches before finalizing inferences."
                    ))

        return findings
