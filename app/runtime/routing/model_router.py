"""
Scientific Model Router - Unified Model Router
Selects optimal AI model based on multi-attribute expected utility and records provenance.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from app.runtime.routing.routing_optimizer import RoutingOptimizer
from app.runtime.routing.routing_history import ModelRoutingDecisionRecord, routing_history
from app.runtime.routing.routing_statistics import routing_statistics
from app.runtime.routing.routing_validator import RoutingValidator


class ScientificModelRouter:
    """Selects the mathematically optimal model for a given extraction or reasoning task."""

    @classmethod
    def route_task(
        cls,
        task_id: str,
        document_complexity: float = 0.5,
        token_estimate: int = 2500,
        weights: Optional[Dict[str, float]] = None,
        max_budget_usd: Optional[float] = None,
        max_latency_ms: Optional[float] = None,
    ) -> Dict[str, Any]:
        candidates = RoutingOptimizer.evaluate_models(
            document_complexity=document_complexity,
            token_estimate=token_estimate,
            weights=weights,
            max_budget_usd=max_budget_usd,
            max_latency_ms=max_latency_ms,
        )

        selected = candidates[0]

        # Invariant validation
        is_valid, errors = RoutingValidator.validate_selection(selected, candidates)

        reason = (
            f"Selected {selected['display_name']} maximizing utility ({selected['expected_utility']}) "
            f"with expected accuracy {selected['expected_accuracy']*100:.1f}%, latency {selected['expected_latency_ms']}ms, "
            f"and cost ${selected['expected_cost_usd']:.5f}."
        )

        decision_id = f"route_{uuid.uuid4().hex[:8]}"
        record = ModelRoutingDecisionRecord(
            decision_id=decision_id,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            task_id=task_id,
            selected_model=selected["model_id"],
            expected_accuracy=selected["expected_accuracy"],
            expected_cost_usd=selected["expected_cost_usd"],
            expected_latency_ms=selected["expected_latency_ms"],
            expected_utility=selected["expected_utility"],
            candidate_models=candidates,
            selection_reason=reason,
        )

        # Record to history and statistics
        routing_history.record(record)
        routing_statistics.record_selection(selected["model_id"], selected["expected_cost_usd"])

        return {
            "decision_id": decision_id,
            "task_id": task_id,
            "selected_model": selected["model_id"],
            "display_name": selected["display_name"],
            "expected_accuracy": selected["expected_accuracy"],
            "expected_cost_usd": selected["expected_cost_usd"],
            "expected_latency_ms": selected["expected_latency_ms"],
            "expected_utility": selected["expected_utility"],
            "reason": reason,
            "candidates": candidates,
            "is_valid": is_valid,
        }
