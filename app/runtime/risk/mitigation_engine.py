"""
Scientific Risk Engine - Mitigation Engine
Generates prescriptive risk mitigation interventions based on failure probabilities.
"""

from typing import List
from dataclasses import dataclass
from app.runtime.risk.probabilistic_risk import FailureProbabilities


@dataclass
class RiskMitigationAction:
    action_id: str
    target_risk: str
    recommended_action: str
    expected_risk_reduction: float
    cost_impact_usd: float
    latency_impact_ms: float
    auto_applicable: bool


class RiskMitigationEngine:
    """Generates prescriptive mitigations when operational risk breaches safety margins."""

    @staticmethod
    def generate_mitigations(probs: FailureProbabilities, budget_remaining: float = 1.0) -> List[RiskMitigationAction]:
        actions: List[RiskMitigationAction] = []

        # 1. OCR failure mitigation
        if probs.p_ocr_failure > 0.15:
            actions.append(
                RiskMitigationAction(
                    action_id="MIT-OCR-001",
                    target_risk="P(OCR Failure)",
                    recommended_action="Enable dual-engine ensemble (PyTesseract + Vision Transformer Preprocessing)",
                    expected_risk_reduction=round(probs.p_ocr_failure * 0.65, 4),
                    cost_impact_usd=0.005,
                    latency_impact_ms=250.0,
                    auto_applicable=True,
                )
            )

        # 2. Timeout mitigation
        if probs.p_timeout > 0.12:
            actions.append(
                RiskMitigationAction(
                    action_id="MIT-LAT-002",
                    target_risk="P(Timeout)",
                    recommended_action="Route to Gemini Flash with speculative wavefront parallelization",
                    expected_risk_reduction=round(probs.p_timeout * 0.70, 4),
                    cost_impact_usd=-0.002,
                    latency_impact_ms=-800.0,
                    auto_applicable=True,
                )
            )

        # 3. Schema violation mitigation
        if probs.p_schema_violation > 0.10:
            actions.append(
                RiskMitigationAction(
                    action_id="MIT-VAL-003",
                    target_risk="P(Schema Violation)",
                    recommended_action="Inject strict JSON Schema grammar enforcement & secondary field validator",
                    expected_risk_reduction=round(probs.p_schema_violation * 0.80, 4),
                    cost_impact_usd=0.001,
                    latency_impact_ms=80.0,
                    auto_applicable=True,
                )
            )

        # 4. Worker failure mitigation
        if probs.p_worker_failure > 0.08:
            actions.append(
                RiskMitigationAction(
                    action_id="MIT-WRK-004",
                    target_risk="P(Worker Failure)",
                    recommended_action="Hot-swap to high-reputation secondary worker node with health heartbeat check",
                    expected_risk_reduction=round(probs.p_worker_failure * 0.75, 4),
                    cost_impact_usd=0.0,
                    latency_impact_ms=120.0,
                    auto_applicable=True,
                )
            )

        return actions
