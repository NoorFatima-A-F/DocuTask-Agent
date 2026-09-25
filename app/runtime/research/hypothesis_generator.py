"""
Autonomous Research - Hypothesis Generator
Formulates testable scientific hypotheses from observed telemetry anomalies and bottlenecks.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import uuid


@dataclass
class ResearchHypothesis:
    hypothesis_id: str
    target_component: str
    premise: str
    proposed_intervention: str
    expected_primary_metric_impact: str
    risk_level: str  # LOW | MEDIUM | HIGH

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HypothesisGenerator:
    """Generates empirical hypotheses for autonomous exploration."""

    @classmethod
    def generate_hypotheses_from_telemetry(
        cls,
        p95_latency_ms: float,
        avg_cost_usd: float,
        ocr_confidence: float,
    ) -> List[ResearchHypothesis]:
        hypotheses: List[ResearchHypothesis] = []

        if p95_latency_ms > 800.0:
            hypotheses.append(
                ResearchHypothesis(
                    hypothesis_id=f"HYP-{uuid.uuid4().hex[:4].upper()}",
                    target_component="Planner Parallelism & Model Selection",
                    premise="Observed P95 latency is inflated by serialized LLM validation calls.",
                    proposed_intervention="Switch to speculative parallel execution with Flash-Lite early gate.",
                    expected_primary_metric_impact="Latency reduction by ~32% with <0.5% accuracy impact.",
                    risk_level="LOW",
                )
            )

        if avg_cost_usd > 0.005:
            hypotheses.append(
                ResearchHypothesis(
                    hypothesis_id=f"HYP-{uuid.uuid4().hex[:4].upper()}",
                    target_component="Prompt Cache & Token Pruning",
                    premise="Repetitive table schema tokens dominate prompt costs.",
                    proposed_intervention="Enable prompt prefix caching and compressed JSON schema representation.",
                    expected_primary_metric_impact="Cost reduction by ~45%.",
                    risk_level="LOW",
                )
            )

        if ocr_confidence < 0.90:
            hypotheses.append(
                ResearchHypothesis(
                    hypothesis_id=f"HYP-{uuid.uuid4().hex[:4].upper()}",
                    target_component="Adaptive Preprocessing Filter",
                    premise="Noise in low-DPI scan passes induces hallucinated field entities.",
                    proposed_intervention="Insert adaptive Otsu thresholding before OCR engine extraction.",
                    expected_primary_metric_impact="OCR confidence boost by +8.5%.",
                    risk_level="MEDIUM",
                )
            )

        return hypotheses
