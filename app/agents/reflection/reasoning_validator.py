"""
Reasoning Validator.
Validates logical validity, causal chains, and evidence soundness in cognitive reasoning steps.
"""

from typing import List
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.self_critique import CritiqueFinding


class ReasoningValidator:
    """Detects invalid reasoning, non sequiturs, and unsupported leaps in logic."""

    def validate_reasoning(self, trace: ExecutionTraceEnvelope) -> List[CritiqueFinding]:
        """Examines reasoning steps to produce critique findings for unsupported conclusions."""
        findings: List[CritiqueFinding] = []

        for step in trace.reasoning_steps:
            # Check for conclusion without evidence or hypotheses
            if not step.evidence and step.confidence_score > 0.85:
                findings.append(CritiqueFinding(
                    category="UNCHECKED_ASSUMPTION",
                    severity="MEDIUM",
                    description=f"High confidence assertion made in step '{step.step_id}' without supporting evidence.",
                    evidence=[f"Conclusion: {step.conclusion}", f"Reported confidence: {step.confidence_score}"],
                    suggested_correction="Ground future inferences in verified tool outputs or domain facts."
                ))

            # Check for circular reasoning (conclusion literally in rationale or assumption)
            if step.conclusion.lower().strip() in [a.lower().strip() for a in step.assumptions]:
                findings.append(CritiqueFinding(
                    category="CIRCULAR_REASONING",
                    severity="HIGH",
                    description=f"Circular reasoning detected in step '{step.step_id}': conclusion assumes itself.",
                    evidence=[f"Conclusion: {step.conclusion}"],
                    suggested_correction="Separate preliminary premises from downstream conclusions."
                ))

        return findings
