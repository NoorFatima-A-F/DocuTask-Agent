"""
AOIS-HROP Phase 13.7 - Runtime Supervisor
Continuously supervises planner, scheduler, workers, optimization, learning, replay, and truth ledger.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from app.runtime.operations.events.operation_events import SubsystemType


@dataclass
class SubsystemSupervisionState:
    subsystem: SubsystemType
    supervised: bool = True
    active_threads: int = 1
    last_action_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = "SUPERVISED_HEALTHY"
    active_missions_count: int = 0
    anomaly_detected: bool = False
    details: Dict[str, Any] = field(default_factory=dict)


class RuntimeSupervisor:
    """
    Supervises core runtime subsystems and enforces supervision invariant policies.
    """

    def __init__(self):
        self._states: Dict[SubsystemType, SubsystemSupervisionState] = {
            st: SubsystemSupervisionState(subsystem=st) for st in SubsystemType
        }

    def inspect_subsystem(self, subsystem: SubsystemType) -> SubsystemSupervisionState:
        state = self._states.get(subsystem)
        if not state:
            state = SubsystemSupervisionState(subsystem=subsystem)
            self._states[subsystem] = state
        state.last_action_timestamp = datetime.now(timezone.utc).isoformat()
        return state

    def update_subsystem_metrics(
        self,
        subsystem: SubsystemType,
        active_threads: int,
        status: str,
        active_missions: int = 0,
        anomaly: bool = False,
        details: Optional[Dict[str, Any]] = None,
    ) -> SubsystemSupervisionState:
        state = self.inspect_subsystem(subsystem)
        state.active_threads = active_threads
        state.status = status
        state.active_missions_count = active_missions
        state.anomaly_detected = anomaly
        if details:
            state.details.update(details)
        state.last_action_timestamp = datetime.now(timezone.utc).isoformat()
        return state

    def get_all_supervision_states(self) -> Dict[str, Dict[str, Any]]:
        return {
            st.value: {
                "subsystem": state.subsystem.value,
                "supervised": state.supervised,
                "active_threads": state.active_threads,
                "status": state.status,
                "active_missions": state.active_missions_count,
                "anomaly_detected": state.anomaly_detected,
                "last_seen": state.last_action_timestamp,
                "details": state.details,
            }
            for st, state in self._states.items()
        }

    def is_all_healthy(self) -> bool:
        return not any(s.anomaly_detected for s in self._states.values())
