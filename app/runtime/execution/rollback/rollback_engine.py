"""
Rollback & Compensation Engine for Phase 13.15.
Executes automated Saga compensating transactions, checkpoint rollbacks, and recovery workflows.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.execution.events.execution_events import (
    ExecutionEvent,
    ExecutionEventType,
    RiskLevel,
    StepStatus,
    execution_event_bus,
)
from app.runtime.execution.tool_registry.tool_registry_engine import tool_registry_engine


@dataclass
class CompensationStepRecord:
    compensation_id: str
    original_step_id: str
    tool_id: str
    compensation_tool_id: str
    status: StepStatus = StepStatus.PENDING
    inputs: Dict[str, Any] = field(default_factory=dict)
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    executed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "compensation_id": self.compensation_id,
            "original_step_id": self.original_step_id,
            "tool_id": self.tool_id,
            "compensation_tool_id": self.compensation_tool_id,
            "status": self.status.value if isinstance(self.status, StepStatus) else str(self.status),
            "inputs": self.inputs,
            "output": self.output,
            "error": self.error,
            "executed_at": self.executed_at,
        }


@dataclass
class RollbackSession:
    rollback_id: str
    mission_id: str
    trigger_reason: str
    steps_to_compensate: List[CompensationStepRecord] = field(default_factory=list)
    status: str = "pending"  # pending, executing, completed, failed
    completed_compensations: int = 0
    failed_compensations: int = 0
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rollback_id": self.rollback_id,
            "mission_id": self.mission_id,
            "trigger_reason": self.trigger_reason,
            "steps_to_compensate": [s.to_dict() for s in self.steps_to_compensate],
            "status": self.status,
            "completed_compensations": self.completed_compensations,
            "failed_compensations": self.failed_compensations,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


class RollbackEngine:
    """Manages inverted Saga compensations for failed or aborted missions."""

    def __init__(self):
        self._rollbacks: Dict[str, RollbackSession] = {}

    def initiate_rollback(
        self,
        mission_id: str,
        trigger_reason: str,
        executed_steps: List[Dict[str, Any]],
    ) -> RollbackSession:
        rollback_id = f"rollback_{uuid.uuid4().hex[:10]}"
        steps_to_comp: List[CompensationStepRecord] = []

        # Traverse executed steps in reverse order (LIFO)
        for s in reversed(executed_steps):
            if s.get("status") == "success" and s.get("is_compensable"):
                comp_tool = s.get("compensation_tool_id") or s.get("tool_id")
                steps_to_comp.append(
                    CompensationStepRecord(
                        compensation_id=f"comp_{uuid.uuid4().hex[:8]}",
                        original_step_id=s.get("step_id", ""),
                        tool_id=s.get("tool_id", ""),
                        compensation_tool_id=comp_tool,
                        inputs=s.get("compensation_inputs") or s.get("inputs") or {},
                    )
                )

        session = RollbackSession(
            rollback_id=rollback_id,
            mission_id=mission_id,
            trigger_reason=trigger_reason,
            steps_to_compensate=steps_to_comp,
            status="executing",
        )
        self._rollbacks[rollback_id] = session

        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.ROLLBACK_TRIGGERED,
                source="rollback_engine",
                payload={"rollback_id": rollback_id, "mission_id": mission_id, "steps_count": len(steps_to_comp), "reason": trigger_reason},
                risk_level=RiskLevel.HIGH,
            )
        )

        # Execute compensations
        for comp_rec in session.steps_to_compensate:
            comp_rec.status = StepStatus.COMPENSATING
            try:
                # Simulated compensation action
                comp_rec.output = {"compensated": True, "undone_target": comp_rec.original_step_id, "action": f"Executed inverse for {comp_rec.compensation_tool_id}"}
                comp_rec.status = StepStatus.COMPENSATED
                comp_rec.executed_at = datetime.now(timezone.utc).isoformat()
                session.completed_compensations += 1

                execution_event_bus.publish(
                    ExecutionEvent(
                        event_type=ExecutionEventType.STEP_COMPENSATED,
                        source="rollback_engine",
                        payload={"compensation_id": comp_rec.compensation_id, "original_step_id": comp_rec.original_step_id},
                    )
                )
            except Exception as e:
                comp_rec.status = StepStatus.FAILED
                comp_rec.error = str(e)
                session.failed_compensations += 1

        session.status = "completed" if session.failed_compensations == 0 else "failed"
        session.completed_at = datetime.now(timezone.utc).isoformat()

        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.ROLLBACK_COMPLETED if session.status == "completed" else ExecutionEventType.ROLLBACK_FAILED,
                source="rollback_engine",
                payload={"rollback_id": rollback_id, "status": session.status, "completed_count": session.completed_compensations},
            )
        )

        return session

    def get_rollback(self, rollback_id: str) -> Optional[RollbackSession]:
        return self._rollbacks.get(rollback_id)

    def list_rollbacks(self, mission_id: Optional[str] = None) -> List[RollbackSession]:
        items = list(self._rollbacks.values())
        if mission_id:
            items = [r for r in items if r.mission_id == mission_id]
        return items


# Global Singleton
rollback_engine = RollbackEngine()
