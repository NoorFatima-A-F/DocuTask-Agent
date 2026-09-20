"""
Telemetry Reconstructor for Phase 13.4.
Rebuilds flame graphs, step latencies, cost, and energy expenditures from events.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ReconstructedTelemetryState(BaseModel):
    total_duration_ms: float = 0.0
    total_cost_usd: float = 0.0
    total_tokens_consumed: int = 0
    subsystem_latencies_ms: Dict[str, float] = Field(default_factory=dict)
    step_timings: List[Dict[str, Any]] = Field(default_factory=list)


class TelemetryReconstructor:
    """
    Reconstructs execution timeline metrics and resource consumption from events.
    """

    @classmethod
    def reconstruct_from_events(
        cls,
        events: List[Dict[str, Any]],
        target_cursor: Optional[int] = None,
    ) -> ReconstructedTelemetryState:
        state = ReconstructedTelemetryState()
        sliced = events[: (target_cursor + 1)] if target_cursor is not None else events

        for ev in sliced:
            evt_type = ev.get("event_type") or ev.get("type", "")
            payload = ev.get("payload", {})

            if "duration_ms" in payload:
                dur = float(payload["duration_ms"])
                state.total_duration_ms += dur
                sub = payload.get("subsystem", evt_type.split(".")[0])
                state.subsystem_latencies_ms[sub] = state.subsystem_latencies_ms.get(sub, 0.0) + dur

            if "cost_usd" in payload:
                state.total_cost_usd += float(payload["cost_usd"])

            if "tokens_used" in payload or "prompt_tokens" in payload:
                tokens = int(payload.get("tokens_used", 0) or payload.get("prompt_tokens", 0))
                state.total_tokens_consumed += tokens

            if "step.completed" in evt_type or "task_completed" in evt_type:
                state.step_timings.append({
                    "event_id": ev.get("event_id"),
                    "name": payload.get("task_id") or payload.get("task_type") or evt_type,
                    "duration_ms": float(payload.get("duration_ms", 0.0)),
                    "timestamp": ev.get("timestamp"),
                })

        return state
