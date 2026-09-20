"""
Critique Engine.
Orchestrates self-critique generation, reasoning validation, hallucination detection,
inconsistency detection, and bias auditing across execution traces.
"""

from typing import List, Optional
from uuid import uuid4
from app.agents.reflection.bias_detector import BiasDetector
from app.agents.reflection.evaluation import EvaluationReport
from app.agents.reflection.hallucination_detector import HallucinationDetector
from app.agents.reflection.inconsistency_detector import InconsistencyDetector
from app.agents.reflection.interfaces import ICritiqueEngine
from app.agents.reflection.reasoning_validator import ReasoningValidator
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.self_critique import CritiqueFinding, SelfCritique


class CritiqueEngine(ICritiqueEngine):
    """Generates structured self-critique across reasoning, actions, and execution outcomes."""

    def __init__(
        self,
        reasoning_validator: Optional[ReasoningValidator] = None,
        hallucination_detector: Optional[HallucinationDetector] = None,
        inconsistency_detector: Optional[InconsistencyDetector] = None,
        bias_detector: Optional[BiasDetector] = None
    ):
        self.reasoning_validator = reasoning_validator or ReasoningValidator()
        self.hallucination_detector = hallucination_detector or HallucinationDetector()
        self.inconsistency_detector = inconsistency_detector or InconsistencyDetector()
        self.bias_detector = bias_detector or BiasDetector()

    def generate_critique(
        self,
        trace: ExecutionTraceEnvelope,
        evaluation_report: EvaluationReport
    ) -> SelfCritique:
        """Synthesizes all critical findings into a SelfCritique aggregate."""
        findings: List[CritiqueFinding] = []

        # Run specialized detectors
        findings.extend(self.reasoning_validator.validate_reasoning(trace))
        findings.extend(self.hallucination_detector.detect_hallucinations(trace))
        findings.extend(self.inconsistency_detector.detect_inconsistencies(trace))
        findings.extend(self.bias_detector.detect_bias(trace))

        # Identify weaknesses and strengths
        strengths = list(evaluation_report.key_strengths)
        weaknesses = list(evaluation_report.key_weaknesses)

        for f in findings:
            weaknesses.append(f"[{f.category}] {f.description}")

        # Derive opportunities
        opportunities: List[str] = []
        if any(f.category == "HALLUCINATION" for f in findings):
            opportunities.append("Incorporate pre-execution factual verification steps in the planner.")
        if any(f.category == "SUBOPTIMAL_PLAN" or f.category == "UNCHECKED_ASSUMPTION" for f in findings):
            opportunities.append("Strengthen dependency validation before dispatching task graphs.")
        if not opportunities and len(weaknesses) == 0:
            opportunities.append("Standardize this decomposition strategy as an exemplar pattern.")

        # Compute critique score: 1.0 down to 0.0 based on findings severity
        critique_score = 1.0
        for f in findings:
            if f.severity == "CRITICAL":
                critique_score -= 0.3
            elif f.severity == "HIGH":
                critique_score -= 0.15
            elif f.severity == "MEDIUM":
                critique_score -= 0.05
        critique_score = max(0.0, min(1.0, critique_score))

        return SelfCritique(
            critique_id=uuid4(),
            execution_id=trace.execution_id,
            strengths=strengths,
            weaknesses=weaknesses,
            findings=findings,
            missed_opportunities=[f.suggested_correction for f in findings if f.suggested_correction],
            improvement_opportunities=opportunities,
            confidence_explanation=f"Critique synthesized from {len(findings)} findings with score {critique_score:.2f}.",
            uncertainty_analysis={"findings_count": len(findings), "critical_issues": sum(1 for f in findings if f.severity == "CRITICAL")},
            overall_critique_score=critique_score
        )
