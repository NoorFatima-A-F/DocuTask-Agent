"""
Deterministic Replay Validator.
Mathematically asserts that replaying an immutable event log multiple times produces identical state.
"""

from typing import List
from pydantic import BaseModel, Field
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.replay.replay_state_machine import ReplayStateMachine, ReconstructedMissionState


class DeterminismValidationReport(BaseModel):
    mission_id: str
    is_deterministic: bool = Field(..., description="True if repeated replay produces bitwise identical state")
    runs_evaluated: int = Field(..., description="Number of validation runs executed")
    state_diffs_found: int = Field(default=0, description="Number of differences found (must be 0)")
    verification_hash: str = Field(..., description="State integrity hash")


class ReplayValidator:
    """Verifies that Replay(Log_1) == Replay(Log_1) deterministically."""

    @staticmethod
    def validate_determinism(mission_id: str, events: List[RuntimeEvent], repetitions: int = 3) -> DeterminismValidationReport:
        if repetitions < 2:
            repetitions = 2

        states: List[ReconstructedMissionState] = []
        for _ in range(repetitions):
            state = ReplayStateMachine.create_initial_state(mission_id)
            for e in events:
                state = ReplayStateMachine.apply_event(state, e)
            states.append(state)

        # Compare state[0] against all other runs
        base_state = states[0]
        base_dump = base_state.model_dump_json()

        diffs_count = 0
        for i in range(1, repetitions):
            if states[i].model_dump_json() != base_dump:
                diffs_count += 1

        import hashlib
        state_hash = hashlib.sha256(base_dump.encode("utf-8")).hexdigest()

        return DeterminismValidationReport(
            mission_id=mission_id,
            is_deterministic=(diffs_count == 0),
            runs_evaluated=repetitions,
            state_diffs_found=diffs_count,
            verification_hash=state_hash,
        )
