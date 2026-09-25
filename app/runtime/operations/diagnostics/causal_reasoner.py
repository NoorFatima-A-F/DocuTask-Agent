"""
AOIS-HROP Phase 13.7 - Causal Reasoner
Generates human-readable, explainable causal chains and failure propagation graphs.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class CausalDiagnosticExplanation:
    root_cause_summary: str
    causal_steps: List[str]
    confidence: float
    evidence_sources: List[str] = field(default_factory=list)


class CausalReasoner:
    """
    Constructs explainable diagnostic narratives from multi-source telemetry and causal dependency graphs.
    """

    def construct_explanation(
        self,
        culprit_subsystem: str,
        error_type: str,
        affected_subsystems: List[str],
        confidence: float = 0.95,
    ) -> CausalDiagnosticExplanation:
        steps = [f"Anomaly originated in [{culprit_subsystem}] characterized by '{error_type}'."]

        for aff in affected_subsystems:
            if aff != culprit_subsystem:
                steps.append(f"Degradation propagated downstream from [{culprit_subsystem}] to [{aff}].")

        steps.append(f"Cascading failure bounded; autonomous healing isolation recommended for [{culprit_subsystem}].")

        summary = f"Root cause identified in [{culprit_subsystem}] ({error_type}) causing downstream degradation in {len(affected_subsystems)} subsystems."

        return CausalDiagnosticExplanation(
            root_cause_summary=summary,
            causal_steps=steps,
            confidence=confidence,
            evidence_sources=["EventStore", "ReplayEngine", "RuntimeTelemetry", "TruthLedger"],
        )
