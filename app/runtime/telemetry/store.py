# Runtime Telemetry Store
from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.runtime.events.base import RuntimeEvent
from app.runtime.events.persistence import EventStore

@dataclass
class AgentLiveState:
    agent_id: str
    role_name: str
    state: str = 'IDLE'
    last_event_type: str = 'INITIALIZED'
    last_active_utc: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    current_task_id: Optional[str] = None
    completed_task_count: int = 0
    failed_task_count: int = 0
    error_message: Optional[str] = None

@dataclass
class TaskDagNodeState:
    node_id: str
    title: str
    stage: str = 'EXECUTE'
    status: str = 'PENDING'
    assigned_agent_id: Optional[str] = None
    assigned_worker_id: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[float] = None
    confidence_score: Optional[float] = None
    error_message: Optional[str] = None

@dataclass
class MissionLiveState:
    mission_id: str
    goal: str
    current_state: str = 'IDLE'
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    total_events_count: int = 0
    total_tasks_count: int = 0
    completed_tasks_count: int = 0
    failed_tasks_count: int = 0
    retries_count: int = 0
    memory_lookups_count: int = 0
    memory_hits_count: int = 0
    reflection_events_count: int = 0
    latest_confidence_score: float = 0.0
    latest_thought_text: Optional[str] = None
    latest_thought_agent: Optional[str] = None

class RuntimeTelemetryStore:
    def __init__(self, event_store: Optional[EventStore] = None):
        self.event_store = event_store or EventStore()
        self.missions: Dict[str, MissionLiveState] = {}
        self.agents: Dict[str, AgentLiveState] = {}
        self.dag_nodes: Dict[str, Dict[str, TaskDagNodeState]] = {}
        self.recent_events: List[RuntimeEvent] = []
        self._lock = asyncio.Lock()
        self._init_default_agents()

    def _init_default_agents(self):
        roles = [('PLANNER', 'Goal Planner'), ('COORDINATOR', 'Coordinator'), ('VISION', 'Vision Specialist'), ('EXTRACTION', 'Extraction'), ('VALIDATION', 'Validator'), ('EVIDENCE', 'Evidence Ledger'), ('MEMORY', 'Causal Memory'), ('REFLECTION', 'Reflection Engine'), ('STATISTICS', 'Statistical Estimator'), ('GOVERNANCE', 'Governance Policy')]
        for r, n in roles:
            self.agents[r] = AgentLiveState(agent_id=r, role_name=n)

    async def apply_event(self, event: RuntimeEvent):
        async with self._lock:
            self.recent_events.append(event)
            m_id = event.mission_id or 'default_mission'
            if m_id not in self.missions:
                self.missions[m_id] = MissionLiveState(mission_id=m_id, goal=event.payload.get('goal', 'Document Mission'))
            m = self.missions[m_id]
            m.total_events_count += 1
            m.updated_at = event.timestamp
            if event.agent_id in self.agents:
                self.agents[event.agent_id].last_active_utc = event.timestamp
                if event.event_type == 'WorkerStarted':
                    self.agents[event.agent_id].state = 'RUNNING'
                elif event.event_type in ('WorkerCompleted', 'PlannerCompleted', 'ReflectionCompleted'):
                    self.agents[event.agent_id].state = 'IDLE'

    async def get_mission_state(self, mission_id: str):
        async with self._lock:
            return self.missions.get(mission_id)

    async def get_dag_nodes(self, mission_id: str):
        async with self._lock:
            return list(self.dag_nodes.get(mission_id, {}).values())

_GLOBAL_TELEMETRY_STORE: Optional[RuntimeTelemetryStore] = None

# Alias for backward compatibility
TelemetryStore = RuntimeTelemetryStore

def get_global_telemetry_store():
    global _GLOBAL_TELEMETRY_STORE
    if _GLOBAL_TELEMETRY_STORE is None:
        _GLOBAL_TELEMETRY_STORE = RuntimeTelemetryStore()
    return _GLOBAL_TELEMETRY_STORE

