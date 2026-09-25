"""
Deterministic Replay State Machine for Event-Sourced Mission Replay.
Reconstructs cumulative mission execution state exclusively from events without side effects.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from app.runtime.observability.schemas import RuntimeEvent, EventCategory, EventType


class ReconstructedTaskState(BaseModel):
    task_id: str
    task_type: str
    status: str
    assigned_worker: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: Optional[float] = None
    cost_usd: float = 0.0
    error: Optional[str] = None
    retry_count: int = 0


class ReconstructedMissionState(BaseModel):
    mission_id: str
    status: str = "INITIALIZED"
    generation: int = 1
    total_events_applied: int = 0
    completed_tasks: List[str] = Field(default_factory=list)
    failed_tasks: List[str] = Field(default_factory=list)
    running_tasks: List[str] = Field(default_factory=list)
    tasks: Dict[str, ReconstructedTaskState] = Field(default_factory=dict)
    active_workers: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    cumulative_cost_usd: float = 0.0
    recovery_count: int = 0
    mutations_applied: int = 0
    human_interventions: List[Dict[str, Any]] = Field(default_factory=list)
    reflections_recorded: List[Dict[str, Any]] = Field(default_factory=list)
    governance_passed: bool = True
    last_event_id: Optional[str] = None
    last_event_type: Optional[str] = None
    last_timestamp: Optional[str] = None

    def clone(self) -> "ReconstructedMissionState":
        """Creates a deep copy of the current state."""
        return ReconstructedMissionState.model_validate(self.model_dump())


class ReplayStateMachine:
    """Pure functional deterministic state transition machine."""

    @staticmethod
    def create_initial_state(mission_id: str) -> ReconstructedMissionState:
        return ReconstructedMissionState(mission_id=mission_id)

    @staticmethod
    def apply_event(state: ReconstructedMissionState, event: RuntimeEvent) -> ReconstructedMissionState:
        """Applies a single RuntimeEvent transition to the state and returns updated state."""
        state.total_events_applied += 1
        state.last_event_id = event.event_id
        state.last_event_type = event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type)
        ts_str = str(event.timestamp)
        state.last_timestamp = ts_str

        cat_str = event.category.value if hasattr(event.category, "value") else str(event.category)
        etype_str = event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type)

        # Mission Lifecycle Events
        if cat_str == "MISSION" or event.category == EventCategory.MISSION:
            if etype_str == "MISSION_STARTED" or event.event_type == EventType.MISSION_STARTED:
                state.status = "RUNNING"
            elif etype_str == "MISSION_COMPLETED" or event.event_type == EventType.MISSION_COMPLETED:
                state.status = "COMPLETED"
            elif etype_str in {"MISSION_FAILED", "MISSION_ABORTED"} or event.event_type in {EventType.MISSION_FAILED, EventType.MISSION_ABORTED}:
                state.status = "FAILED"

        # Planner & Generation Events
        elif cat_str == "PLANNER" or event.category == EventCategory.PLANNER:
            if "generation" in event.payload:
                state.generation = int(event.payload["generation"])
            if etype_str == "PLANNER_STRATEGY_MUTATED" or "mutation" in etype_str.lower():
                state.mutations_applied += 1

        # Task Execution Events
        elif cat_str == "EXECUTION" or event.category == EventCategory.EXECUTION:
            task_id = event.payload.get("task_id") or event.payload.get("node_id") or event.event_id
            task_type = event.payload.get("task_type", "GENERAL")

            if task_id not in state.tasks:
                state.tasks[task_id] = ReconstructedTaskState(
                    task_id=task_id,
                    task_type=task_type,
                    status="INITIALIZED",
                )

            task = state.tasks[task_id]
            task.assigned_worker = event.worker_id or task.assigned_worker

            if etype_str in {"EXECUTION_TASK_STARTED", "EXECUTION_NODE_EXECUTED"} or event.event_type in {EventType.EXECUTION_TASK_STARTED, EventType.EXECUTION_NODE_EXECUTED}:
                task.status = "RUNNING"
                task.started_at = ts_str
                if task_id not in state.running_tasks:
                    state.running_tasks.append(task_id)

            elif etype_str in {"EXECUTION_TASK_COMPLETED", "EXECUTION_STEP_COMPLETED"} or event.event_type in {EventType.EXECUTION_TASK_COMPLETED, EventType.EXECUTION_STEP_COMPLETED}:
                task.status = "COMPLETED"
                task.completed_at = ts_str
                if task_id in state.running_tasks:
                    state.running_tasks.remove(task_id)
                if task_id not in state.completed_tasks:
                    state.completed_tasks.append(task_id)
                if "duration_ms" in event.payload:
                    task.duration_ms = float(event.payload["duration_ms"])

            elif etype_str in {"EXECUTION_TASK_FAILED", "EXECUTION_STEP_FAILED"} or event.event_type in {EventType.EXECUTION_TASK_FAILED, EventType.EXECUTION_STEP_FAILED}:
                task.status = "FAILED"
                task.error = event.payload.get("error", "Task execution failed")
                if task_id in state.running_tasks:
                    state.running_tasks.remove(task_id)
                if task_id not in state.failed_tasks:
                    state.failed_tasks.append(task_id)

        # Worker Allocation
        elif cat_str == "WORKER" or event.category == EventCategory.WORKER:
            if event.worker_id:
                w_state = state.active_workers.setdefault(event.worker_id, {
                    "worker_id": event.worker_id,
                    "status": "ACTIVE",
                    "tasks_processed": 0,
                })
                w_state["last_active"] = ts_str
                if etype_str == "WORKER_TASK_ASSIGNED" or event.event_type == EventType.WORKER_TASK_ASSIGNED:
                    w_state["tasks_processed"] += 1

        # Cost Events
        elif cat_str == "COST" or event.category == EventCategory.COST:
            cost = float(event.payload.get("cost_usd", event.payload.get("amount", 0.0)))
            state.cumulative_cost_usd += cost

        # Failure & Recovery
        elif cat_str == "RECOVERY" or event.category == EventCategory.RECOVERY:
            state.recovery_count += 1
            state.status = "RECOVERING"

        # Human Review
        elif cat_str == "HUMAN_REVIEW" or event.category == EventCategory.HUMAN_REVIEW:
            state.human_interventions.append({
                "event_id": event.event_id,
                "timestamp": ts_str,
                "action": event.payload.get("action", "HUMAN_EDIT"),
                "details": event.payload,
            })

        # Reflection
        elif cat_str == "REFLECTION" or event.category == EventCategory.REFLECTION:
            state.reflections_recorded.append({
                "event_id": event.event_id,
                "timestamp": ts_str,
                "rule": event.payload.get("rule", "Observation recorded"),
            })

        # Governance
        elif cat_str == "GOVERNANCE" or event.category == EventCategory.GOVERNANCE:
            if event.payload.get("passed") is False:
                state.governance_passed = False

        return state
