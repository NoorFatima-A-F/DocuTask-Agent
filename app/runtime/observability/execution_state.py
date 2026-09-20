"""
ARTEICP Observability - Live Execution State Tracker
Thread-safe tracker of active missions, running DAG tasks, worker allocations, and runtime lifecycle states.
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
import time
import threading


@dataclass
class TaskExecutionState:
    task_id: str
    mission_id: str
    task_type: str
    status: str  # WAITING | SCHEDULED | RUNNING | COMPLETED | FAILED | REPLANNED
    assigned_worker_id: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    duration_ms: float = 0.0
    retry_count: int = 0
    confidence_score: float = 0.0
    cost_usd: float = 0.0
    output_summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MissionExecutionSnapshot:
    mission_id: str
    status: str  # PENDING | PLANNING | EXECUTING | ADAPTING | COMPLETED | FAILED
    current_wavefront: int
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    replanned_tasks: int
    active_worker_count: int
    accumulated_cost_usd: float
    elapsed_time_ms: float
    overall_confidence: float
    tasks: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ExecutionStateManager:
    """Thread-safe real-time tracker of live mission execution graphs and task states."""

    def __init__(self):
        self._lock = threading.RLock()
        self._missions: Dict[str, MissionExecutionSnapshot] = {}
        self._tasks: Dict[str, TaskExecutionState] = {}
        self._seed_active_mission()

    def _seed_active_mission(self):
        m_id = "mission_live_001"
        self._missions[m_id] = MissionExecutionSnapshot(
            mission_id=m_id,
            status="EXECUTING",
            current_wavefront=2,
            total_tasks=6,
            completed_tasks=3,
            failed_tasks=0,
            replanned_tasks=0,
            active_worker_count=2,
            accumulated_cost_usd=0.0024,
            elapsed_time_ms=485.0,
            overall_confidence=0.965,
        )
        # Seed tasks
        t1 = TaskExecutionState(
            task_id="task_ocr_0",
            mission_id=m_id,
            task_type="OCR_INGEST",
            status="COMPLETED",
            assigned_worker_id="worker_ocr_1",
            duration_ms=180.0,
            confidence_score=0.97,
            cost_usd=0.0004,
            output_summary="Parsed 4 pages with Tesseract/LayoutLM high confidence",
        )
        t2 = TaskExecutionState(
            task_id="task_extract_1",
            mission_id=m_id,
            task_type="LLM_ENTITY_EXTRACTION",
            status="RUNNING",
            assigned_worker_id="worker_llm_1",
            started_at=time.time() - 0.25,
            confidence_score=0.96,
            cost_usd=0.0012,
        )
        t3 = TaskExecutionState(
            task_id="task_validate_2",
            mission_id=m_id,
            task_type="SCHEMA_CROSS_VALIDATION",
            status="SCHEDULED",
        )
        self._tasks[t1.task_id] = t1
        self._tasks[t2.task_id] = t2
        self._tasks[t3.task_id] = t3
        self._missions[m_id].tasks = {
            t1.task_id: t1.to_dict(),
            t2.task_id: t2.to_dict(),
            t3.task_id: t3.to_dict(),
        }

    def update_task_state(
        self,
        task_id: str,
        mission_id: str,
        status: str,
        task_type: str = "GENERIC_TASK",
        assigned_worker: Optional[str] = None,
        duration_ms: float = 0.0,
        confidence: float = 0.0,
        cost_usd: float = 0.0,
    ) -> TaskExecutionState:
        with self._lock:
            if task_id not in self._tasks:
                self._tasks[task_id] = TaskExecutionState(
                    task_id=task_id,
                    mission_id=mission_id,
                    task_type=task_type,
                    status=status,
                )
            t = self._tasks[task_id]
            t.status = status
            if assigned_worker:
                t.assigned_worker_id = assigned_worker
            if duration_ms > 0:
                t.duration_ms = duration_ms
            if confidence > 0:
                t.confidence_score = confidence
            if cost_usd > 0:
                t.cost_usd = cost_usd

            # Update parent mission
            if mission_id in self._missions:
                m = self._missions[mission_id]
                m.tasks[task_id] = t.to_dict()
                m.completed_tasks = sum(1 for task in m.tasks.values() if task.get("status") == "COMPLETED")
                m.updated_at = time.time()

            return t

    def get_mission_snapshot(self, mission_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            m = self._missions.get(mission_id)
            return m.to_dict() if m else None

    def list_active_missions(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [m.to_dict() for m in self._missions.values()]


execution_state_manager = ExecutionStateManager()
