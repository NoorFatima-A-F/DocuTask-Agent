"""
Decision Trace for Phase 13.4.
Traces planner decisions back to evidence inputs, cost models, and utility calculations.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class DecisionTraceRecord(BaseModel):
    decision_id: str
    decision_type: str
    selected_option: str
    considered_options: List[Dict[str, Any]] = Field(default_factory=list)
    utility_formula: str
    input_events: List[str] = Field(default_factory=list)
    confidence_at_decision: float = 0.95
    timestamp: str


class DecisionTrace:
    """
    Extracts explicit decision provenance traces from replay event streams.
    """

    @classmethod
    def trace_all_decisions(
        cls,
        events: List[Dict[str, Any]],
    ) -> List[DecisionTraceRecord]:
        traces = []
        for ev in events:
            evt_type = ev.get("event_type", "")
            if "decision" in evt_type or "planner.strategy_selected" in evt_type:
                payload = ev.get("payload", {})
                traces.append(DecisionTraceRecord(
                    decision_id=ev.get("event_id", f"dec_{len(traces)}"),
                    decision_type=payload.get("decision_type", "STRATEGY_SELECTION"),
                    selected_option=payload.get("selected_strategy") or payload.get("choice", "optimal"),
                    considered_options=payload.get("options", []),
                    utility_formula=payload.get("utility_formula", "ExpectedUtility = Conf * Rel - Cost"),
                    input_events=[ev.get("causation_id")] if ev.get("causation_id") else [],
                    confidence_at_decision=float(payload.get("confidence", 0.95)),
                    timestamp=ev.get("timestamp", ""),
                ))
        return traces
