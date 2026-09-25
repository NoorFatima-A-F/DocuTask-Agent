"""
Memory Reconstructor for Phase 13.4.
Rebuilds experience retrieval, belief states, and causal memory nodes from event streams.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ReconstructedMemoryState(BaseModel):
    stored_memories: List[Dict[str, Any]] = Field(default_factory=list)
    retrieved_experiences: List[Dict[str, Any]] = Field(default_factory=list)
    active_beliefs: Dict[str, Any] = Field(default_factory=dict)
    memory_hit_ratio: float = 0.0


class MemoryReconstructor:
    """
    Reconstructs agent episodic and semantic memory interactions from events.
    """

    @classmethod
    def reconstruct_from_events(
        cls,
        events: List[Dict[str, Any]],
        target_cursor: Optional[int] = None,
    ) -> ReconstructedMemoryState:
        state = ReconstructedMemoryState()
        sliced = events[: (target_cursor + 1)] if target_cursor is not None else events

        hits = 0
        total_queries = 0

        for ev in sliced:
            evt_type = ev.get("event_type") or ev.get("type", "")
            payload = ev.get("payload", {})

            if "memory.stored" in evt_type or "memory.created" in evt_type:
                state.stored_memories.append(payload)
            elif "memory.retrieved" in evt_type or "experience.queried" in evt_type:
                total_queries += 1
                if payload.get("matches"):
                    hits += 1
                    state.retrieved_experiences.extend(payload["matches"])
            elif "belief.updated" in evt_type:
                k = payload.get("belief_key")
                if k:
                    state.active_beliefs[k] = payload.get("belief_value")

        if total_queries > 0:
            state.memory_hit_ratio = round(hits / total_queries, 3)

        return state
