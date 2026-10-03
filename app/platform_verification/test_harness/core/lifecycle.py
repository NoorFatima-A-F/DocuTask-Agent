"""
Test Lifecycle State Machine enforcing deterministic transitions.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from app.platform_verification.test_harness.domain.models import TestLifecycleState

VALID_TRANSITIONS: Dict[TestLifecycleState, List[TestLifecycleState]] = {
    TestLifecycleState.CREATED: [TestLifecycleState.VALIDATED],
    TestLifecycleState.VALIDATED: [TestLifecycleState.SCHEDULED],
    TestLifecycleState.SCHEDULED: [TestLifecycleState.EXECUTING],
    TestLifecycleState.EXECUTING: [TestLifecycleState.COLLECTING_EVIDENCE],
    TestLifecycleState.COLLECTING_EVIDENCE: [TestLifecycleState.EVALUATING],
    TestLifecycleState.EVALUATING: [TestLifecycleState.COMPLETED],
    TestLifecycleState.COMPLETED: [TestLifecycleState.ARCHIVED],
    TestLifecycleState.ARCHIVED: [],
}


@dataclass
class LifecycleTransitionRecord:
    from_state: TestLifecycleState
    to_state: TestLifecycleState
    timestamp: str
    reason: str


class TestLifecycleManager:
    """Enforces valid state machine transitions for test executions."""
    __test__ = False

    def __init__(self, initial_state: TestLifecycleState = TestLifecycleState.CREATED) -> None:
        self._current_state = initial_state
        self._history: List[LifecycleTransitionRecord] = []

    @property
    def current_state(self) -> TestLifecycleState:
        return self._current_state

    def transition_to(self, new_state: TestLifecycleState, reason: str = "") -> None:
        allowed = VALID_TRANSITIONS.get(self._current_state, [])
        if new_state not in allowed:
            raise ValueError(
                f"Invalid lifecycle transition: cannot transition from '{self._current_state.value}' to '{new_state.value}'."
            )

        record = LifecycleTransitionRecord(
            from_state=self._current_state,
            to_state=new_state,
            timestamp=datetime.now(timezone.utc).isoformat(),
            reason=reason,
        )
        self._history.append(record)
        self._current_state = new_state

    def get_history(self) -> List[LifecycleTransitionRecord]:
        return list(self._history)
