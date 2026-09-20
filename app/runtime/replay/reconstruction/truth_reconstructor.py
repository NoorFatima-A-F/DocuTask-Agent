"""
Truth Reconstructor for Phase 13.4.
Rebuilds Truth Ledger invariants, verified claims, and Merkle root certifications from events.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ReconstructedTruthState(BaseModel):
    verified_invariants: List[Dict[str, Any]] = Field(default_factory=list)
    invariant_violations: List[Dict[str, Any]] = Field(default_factory=list)
    merkle_roots: List[str] = Field(default_factory=list)
    active_ledger_hash: Optional[str] = None
    all_invariants_satisfied: bool = True


class TruthReconstructor:
    """
    Reconstructs mathematical truth proofs and invariant verification states from events.
    """

    @classmethod
    def reconstruct_from_events(
        cls,
        events: List[Dict[str, Any]],
        target_cursor: Optional[int] = None,
    ) -> ReconstructedTruthState:
        state = ReconstructedTruthState()
        sliced = events[: (target_cursor + 1)] if target_cursor is not None else events

        for ev in sliced:
            evt_type = ev.get("event_type") or ev.get("type", "")
            payload = ev.get("payload", {})

            if "truth.invariant.checked" in evt_type or "invariant.evaluated" in evt_type:
                passed = payload.get("passed", True)
                if passed:
                    state.verified_invariants.append(payload)
                else:
                    state.invariant_violations.append(payload)
                    state.all_invariants_satisfied = False

            if "truth.merkle_root.sealed" in evt_type or "merkle.sealed" in evt_type:
                root = payload.get("merkle_root") or payload.get("root_hash")
                if root:
                    state.merkle_roots.append(root)
                    state.active_ledger_hash = root

        return state
