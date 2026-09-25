"""
Counterfactual Simulator - Alternate Planner
Synthesizes candidate counterfactual branches ("What if Gemini Pro?", "What if No Retry?", etc.).
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class CounterfactualCandidate:
    branch_id: str
    decision_type: str  # MODEL_CHOICE | RETRY_POLICY | EXECUTION_TOPOLOGY
    intervention_label: str
    simulated_accuracy: float
    simulated_latency_ms: float
    simulated_cost_usd: float
    simulated_utility: float
    is_counterfactually_superior: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AlternatePlanner:
    """Generates counterfactual alternative plans for post-mortem analysis."""

    @classmethod
    def generate_alternatives(
        cls,
        factual_model: str,
        factual_accuracy: float,
        factual_latency_ms: float,
        factual_cost_usd: float,
        factual_utility: float,
    ) -> List[CounterfactualCandidate]:
        alternatives: List[CounterfactualCandidate] = []

        # 1. Counterfactual: What if Gemini 1.5 Pro?
        cf_pro_acc = min(0.998, factual_accuracy + 0.015)
        cf_pro_lat = factual_latency_ms * 2.8
        cf_pro_cost = factual_cost_usd * 8.5
        cf_pro_u = (cf_pro_acc * 0.45) + max(0.0, 1.0 - (cf_pro_lat / 3000.0)) * 0.25 + max(0.0, 1.0 - (cf_pro_cost / 0.05)) * 0.30
        alternatives.append(
            CounterfactualCandidate(
                branch_id="CF-PRO-001",
                decision_type="MODEL_CHOICE",
                intervention_label="Intervention: Route to Gemini 1.5 Pro",
                simulated_accuracy=round(cf_pro_acc, 4),
                simulated_latency_ms=round(cf_pro_lat, 1),
                simulated_cost_usd=round(cf_pro_cost, 5),
                simulated_utility=round(cf_pro_u, 4),
                is_counterfactually_superior=cf_pro_u > factual_utility,
            )
        )

        # 2. Counterfactual: What if Flash-Lite?
        cf_lite_acc = max(0.88, factual_accuracy - 0.045)
        cf_lite_lat = max(180.0, factual_latency_ms * 0.45)
        cf_lite_cost = max(0.0003, factual_cost_usd * 0.25)
        cf_lite_u = (cf_lite_acc * 0.45) + max(0.0, 1.0 - (cf_lite_lat / 3000.0)) * 0.25 + max(0.0, 1.0 - (cf_lite_cost / 0.05)) * 0.30
        alternatives.append(
            CounterfactualCandidate(
                branch_id="CF-LITE-002",
                decision_type="MODEL_CHOICE",
                intervention_label="Intervention: Route to Gemini Flash-Lite",
                simulated_accuracy=round(cf_lite_acc, 4),
                simulated_latency_ms=round(cf_lite_lat, 1),
                simulated_cost_usd=round(cf_lite_cost, 5),
                simulated_utility=round(cf_lite_u, 4),
                is_counterfactually_superior=cf_lite_u > factual_utility,
            )
        )

        # 3. Counterfactual: What if Zero-Retry Strict Timeout?
        cf_noretry_acc = max(0.85, factual_accuracy - 0.08)
        cf_noretry_lat = max(300.0, factual_latency_ms * 0.70)
        cf_noretry_cost = factual_cost_usd * 0.80
        cf_noretry_u = (cf_noretry_acc * 0.45) + max(0.0, 1.0 - (cf_noretry_lat / 3000.0)) * 0.25 + max(0.0, 1.0 - (cf_noretry_cost / 0.05)) * 0.30
        alternatives.append(
            CounterfactualCandidate(
                branch_id="CF-NORETRY-003",
                decision_type="RETRY_POLICY",
                intervention_label="Intervention: Zero-Retry Strict Fail-Fast Policy",
                simulated_accuracy=round(cf_noretry_acc, 4),
                simulated_latency_ms=round(cf_noretry_lat, 1),
                simulated_cost_usd=round(cf_noretry_cost, 5),
                simulated_utility=round(cf_noretry_u, 4),
                is_counterfactually_superior=cf_noretry_u > factual_utility,
            )
        )

        return alternatives
