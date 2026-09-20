"""
In-Flight Adaptive Execution Monitor.

Monitors intermediate execution outputs (confidence scores, validation invariants,
API latencies) and decides when runtime graph adaptation or replanning is required.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AdaptationTrigger(BaseModel):
    trigger_type: str  # LOW_CONFIDENCE, SMT_FAILED, LATENCY_BREACH, SCHEMA_MISMATCH
    node_id: str
    severity: str = "WARNING"
    observed_value: float
    threshold_value: float
    recommended_action: str  # INJECT_RECOVERY, SWITCH_STRATEGY, RETRY_NODE


class AdaptiveExecutionMonitor:
    """Monitors live node outputs against adaptive replanning thresholds."""

    def __init__(self, min_confidence_threshold: float = 0.70) -> None:
        self.min_confidence_threshold = min_confidence_threshold

    def evaluate_node_output(
        self, node_id: str, output: Dict[str, Any]
    ) -> Optional[AdaptationTrigger]:
        """Checks if node output falls below acceptable confidence or invariant thresholds."""
        # 1. Confidence check
        conf = output.get("confidence")
        if conf is not None and float(conf) < self.min_confidence_threshold:
            return AdaptationTrigger(
                trigger_type="LOW_CONFIDENCE",
                node_id=node_id,
                severity="WARNING",
                observed_value=float(conf),
                threshold_value=self.min_confidence_threshold,
                recommended_action="INJECT_RECOVERY",
            )

        # 2. SMT / Validation check
        if output.get("validation_passed") is False:
            return AdaptationTrigger(
                trigger_type="SMT_FAILED",
                node_id=node_id,
                severity="ERROR",
                observed_value=0.0,
                threshold_value=1.0,
                recommended_action="INJECT_RECOVERY",
            )

        return None
