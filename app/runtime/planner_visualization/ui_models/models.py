"""
Pydantic models for Phase 13.2 Autonomous Planner Execution Visualization (APEV-DAG).
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PlannerStateEnum(str, Enum):
    CREATED = "CREATED"
    INITIALIZING = "INITIALIZING"
    CONTEXT_LOADING = "CONTEXT_LOADING"
    MEMORY_SEARCH = "MEMORY_SEARCH"
    CAPABILITY_DISCOVERY = "CAPABILITY_DISCOVERY"
    GOAL_ANALYSIS = "GOAL_ANALYSIS"
    PLAN_SYNTHESIS = "PLAN_SYNTHESIS"
    TASK_DECOMPOSITION = "TASK_DECOMPOSITION"
    DEPENDENCY_ANALYSIS = "DEPENDENCY_ANALYSIS"
    WORKER_ASSIGNMENT = "WORKER_ASSIGNMENT"
    READY = "READY"
    EXECUTING = "EXECUTING"
    REPLANNING = "REPLANNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskNodeType(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    SPLIT = "SPLIT"
    MERGE = "MERGE"
    CONDITIONAL = "CONDITIONAL"
    RETRY = "RETRY"
    RECOVERY = "RECOVERY"
    BARRIER = "BARRIER"
    JOIN = "JOIN"


class TaskExecutionState(str, Enum):
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    RETRY = "RETRY"
    RECOVERY = "RECOVERY"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class GoalObjective(BaseModel):
    goal_id: str
    title: str
    priority: str = "HIGH"
    deadline_ms: float = 30000.0
    estimated_cost_usd: float = 0.003
    estimated_latency_ms: float = 180.0
    confidence: float = 0.95
    required_tools: List[str] = Field(default_factory=list)
    required_memory: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    sub_objectives: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)


class PlannerDAGNode(BaseModel):
    node_id: str
    name: str
    node_type: TaskNodeType = TaskNodeType.SEQUENTIAL
    state: TaskExecutionState = TaskExecutionState.WAITING
    parent_ids: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    assigned_worker: Optional[str] = None
    priority: int = 1
    estimated_cost_usd: float = 0.0005
    estimated_duration_ms: float = 120.0
    actual_duration_ms: Optional[float] = None
    confidence: float = 0.98
    event_id: Optional[str] = None
    truth_ledger_hash: Optional[str] = None
    replay_offset: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PlannerDAGEdge(BaseModel):
    source: str
    target: str
    condition: Optional[str] = None
    edge_type: str = "DATA_DEPENDENCY"


class PlannerDAGSnapshot(BaseModel):
    mission_id: str
    version: int = 1
    state: PlannerStateEnum = PlannerStateEnum.READY
    nodes: List[PlannerDAGNode] = Field(default_factory=list)
    edges: List[PlannerDAGEdge] = Field(default_factory=list)
    critical_path: List[str] = Field(default_factory=list)
    critical_path_duration_ms: float = 0.0
    total_nodes: int = 0
    completed_nodes: int = 0
    updated_at: str = ""


class WorkerAssignmentRecord(BaseModel):
    task_id: str
    task_name: str
    worker_id: str
    worker_role: str
    capability_match_score: float = 0.98
    reason: str
    estimated_time_ms: float = 120.0
    expected_cost_usd: float = 0.0005
    confidence: float = 0.96
    status: str = "ASSIGNED"


class PlannerDecisionCard(BaseModel):
    decision_id: str
    mission_id: str
    decision_type: str
    title: str
    reason: str
    evidence: str
    alternatives_considered: List[Dict[str, Any]] = Field(default_factory=list)
    chosen_alternative: str
    confidence: float = 0.92
    event_id: str
    truth_ledger_hash: str
    replay_offset: int
    timestamp: str


class PlannerMetrics(BaseModel):
    tasks_generated: int = 0
    tasks_running: int = 0
    tasks_waiting: int = 0
    tasks_retried: int = 0
    tasks_replanned: int = 0
    nodes_split: int = 0
    workers_active: int = 0
    scheduler_decisions: int = 0
    average_queue_time_ms: float = 0.0
    critical_path_ms: float = 0.0
    parallelism_factor: float = 1.0
    branching_factor: float = 1.0
    total_cost_usd: float = 0.0
