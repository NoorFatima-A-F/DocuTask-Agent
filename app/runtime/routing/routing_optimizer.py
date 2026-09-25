"""
Scientific Model Router - Routing Optimizer
Optimizes multi-attribute utility for model selection under budget and deadline constraints.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ModelProfile:
    model_id: str
    display_name: str
    base_accuracy: float
    cost_per_1k_tokens_usd: float
    typical_latency_ms: float
    max_context_tokens: int
    specialization: str
    inherent_risk: float


# Registered Model Pool
AVAILABLE_MODELS: List[ModelProfile] = [
    ModelProfile(
        model_id="gemini-1.5-pro",
        display_name="Gemini 1.5 Pro",
        base_accuracy=0.985,
        cost_per_1k_tokens_usd=0.007,
        typical_latency_ms=2200.0,
        max_context_tokens=1000000,
        specialization="Complex Multimodal / Dense Tables / Reasoning",
        inherent_risk=0.02,
    ),
    ModelProfile(
        model_id="gemini-1.5-flash",
        display_name="Gemini 1.5 Flash",
        base_accuracy=0.950,
        cost_per_1k_tokens_usd=0.0005,
        typical_latency_ms=650.0,
        max_context_tokens=1000000,
        specialization="High-Throughput / Extraction / Fast Latency",
        inherent_risk=0.04,
    ),
    ModelProfile(
        model_id="gemini-flash-lite",
        display_name="Gemini Flash Lite",
        base_accuracy=0.910,
        cost_per_1k_tokens_usd=0.00015,
        typical_latency_ms=300.0,
        max_context_tokens=500000,
        specialization="Low-Cost Batch / Pre-Classification",
        inherent_risk=0.08,
    ),
    ModelProfile(
        model_id="local-ocr-specialist",
        display_name="Local PyTesseract / LayoutLM",
        base_accuracy=0.880,
        cost_per_1k_tokens_usd=0.0000,
        typical_latency_ms=180.0,
        max_context_tokens=10000,
        specialization="Zero-Cost Local Preprocessing & OCR",
        inherent_risk=0.12,
    ),
]


class RoutingOptimizer:
    """Computes expected utility for each candidate model given document complexity and constraints."""

    @classmethod
    def evaluate_models(
        cls,
        document_complexity: float,
        token_estimate: int,
        weights: Optional[Dict[str, float]] = None,
        max_budget_usd: Optional[float] = None,
        max_latency_ms: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        w = weights or {"accuracy": 0.45, "cost": 0.25, "latency": 0.20, "risk": 0.10}

        evaluated: List[Dict[str, Any]] = []

        for model in AVAILABLE_MODELS:
            # Adjust expected accuracy by document complexity
            # Complex documents degrade simpler models more heavily
            complexity_penalty = document_complexity * (0.02 if "pro" in model.model_id else 0.08)
            expected_acc = max(0.5, model.base_accuracy - complexity_penalty)

            # Estimated cost
            estimated_cost = (token_estimate / 1000.0) * model.cost_per_1k_tokens_usd

            # Estimated latency (scales slightly with tokens)
            estimated_lat = model.typical_latency_ms + (token_estimate / 500.0) * 10.0

            # Check hard feasibility bounds
            is_feasible = True
            if max_budget_usd is not None and estimated_cost > max_budget_usd:
                is_feasible = False
            if max_latency_ms is not None and estimated_lat > max_latency_ms:
                is_feasible = False

            # Normalized dimensions for utility (0 to 1)
            u_acc = expected_acc
            u_cost = max(0.0, 1.0 - (estimated_cost / 0.05))
            u_lat = max(0.0, 1.0 - (estimated_lat / 3000.0))
            u_risk = max(0.0, 1.0 - model.inherent_risk)

            # Expected utility
            utility = (
                w.get("accuracy", 0.45) * u_acc +
                w.get("cost", 0.25) * u_cost +
                w.get("latency", 0.20) * u_lat +
                w.get("risk", 0.10) * u_risk
            )

            if not is_feasible:
                utility *= 0.1  # Heavy penalty for infeasible candidates

            evaluated.append({
                "model_id": model.model_id,
                "display_name": model.display_name,
                "expected_accuracy": round(expected_acc, 4),
                "expected_cost_usd": round(estimated_cost, 5),
                "expected_latency_ms": round(estimated_lat, 1),
                "inherent_risk": round(model.inherent_risk, 4),
                "expected_utility": round(utility, 4),
                "is_feasible": is_feasible,
                "specialization": model.specialization,
            })

        # Sort descending by expected utility
        evaluated.sort(key=lambda m: m["expected_utility"], reverse=True)
        return evaluated
