"""
Autonomous Runtime Observability Layer (AROL) - Event Taxonomy & Schemas.

Defines strongly typed event models for 19 distinct taxonomies, distributed trace contexts,
metric definitions, snapshot schemas, and runtime health evaluations.
All metrics and states are derived from these immutable events.
"""

from __future__ import annotations

import enum
import time
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EventSeverity(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EventPriority(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"


class EventCategory(str, enum.Enum):
    MISSION = "MISSION"
    PLANNER = "PLANNER"
    EXECUTION = "EXECUTION"
    WORKER = "WORKER"
    RESOURCE = "RESOURCE"
    MEMORY = "MEMORY"
    REFLECTION = "REFLECTION"
    GOVERNANCE = "GOVERNANCE"
    VALIDATION = "VALIDATION"
    TOOL = "TOOL"
    STORAGE = "STORAGE"
    COST = "COST"
    SCHEDULER = "SCHEDULER"
    FAILURE = "FAILURE"
    RECOVERY = "RECOVERY"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    TELEMETRY = "TELEMETRY"
    BENCHMARK = "BENCHMARK"
    SYSTEM = "SYSTEM"


class EventType(str, enum.Enum):
    MISSION_STARTED = "MISSION_STARTED"
    MISSION_COMPLETED = "MISSION_COMPLETED"
    MISSION_FAILED = "MISSION_FAILED"
    MISSION_ABORTED = "MISSION_ABORTED"
    PLANNER_STRATEGY_SELECTED = "PLANNER_STRATEGY_SELECTED"
    PLANNER_STRATEGY_MUTATED = "PLANNER_STRATEGY_MUTATED"
    PLANNER_DAG_GENERATED = "PLANNER_DAG_GENERATED"
    EXECUTION_TASK_STARTED = "EXECUTION_TASK_STARTED"
    EXECUTION_TASK_COMPLETED = "EXECUTION_TASK_COMPLETED"
    EXECUTION_TASK_FAILED = "EXECUTION_TASK_FAILED"
    EXECUTION_STEP_COMPLETED = "EXECUTION_STEP_COMPLETED"
    EXECUTION_STEP_FAILED = "EXECUTION_STEP_FAILED"
    EXECUTION_NODE_EXECUTED = "EXECUTION_NODE_EXECUTED"
    WORKER_TASK_ASSIGNED = "WORKER_TASK_ASSIGNED"
    WORKER_TASK_COMPLETED = "WORKER_TASK_COMPLETED"
    GOVERNANCE_RULE_EVALUATED = "GOVERNANCE_RULE_EVALUATED"
    REFLECTION_RULE_PROPOSED = "REFLECTION_RULE_PROPOSED"
    HUMAN_REVIEW_REQUESTED = "HUMAN_REVIEW_REQUESTED"
    HUMAN_REVIEW_COMPLETED = "HUMAN_REVIEW_COMPLETED"


class TraceContext(BaseModel):
    """OpenTelemetry-compatible distributed trace context."""
    trace_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    span_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    parent_span_id: Optional[str] = None
    execution_depth: int = 0
    component: str = "runtime"
    operation: str = "execute"
    worker_id: Optional[str] = None
    node_id: Optional[str] = None
    timestamp_ns: int = Field(default_factory=time.time_ns)
    baggage: Dict[str, str] = Field(default_factory=dict)


class BaseRuntimeEvent(BaseModel):
    """Base immutable runtime event containing comprehensive provenance metadata."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: EventCategory
    event_type: str
    mission_id: str
    sequence_number: int = 0
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_event_id: Optional[str] = None
    trace_context: TraceContext = Field(default_factory=TraceContext)
    timestamp: float = Field(default_factory=time.time)
    duration_ms: float = 0.0
    agent_id: Optional[str] = None
    worker_id: Optional[str] = None
    node_id: Optional[str] = None
    task_id: Optional[str] = None
    stage: str = "execution"
    status: str = "SUCCESS"
    severity: EventSeverity = EventSeverity.INFO
    priority: EventPriority = EventPriority.NORMAL
    payload: Dict[str, Any] = Field(default_factory=dict)
    evidence: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    version: str = "1.0.0"
    prev_event_hash: Optional[str] = None
    event_hash: Optional[str] = None

    @property
    def hash(self) -> Optional[str]:
        return self.event_hash

    @hash.setter
    def hash(self, val: Optional[str]) -> None:
        self.event_hash = val

    @property
    def previous_hash(self) -> Optional[str]:
        return self.prev_event_hash

    @previous_hash.setter
    def previous_hash(self, val: Optional[str]) -> None:
        self.prev_event_hash = val


RuntimeEvent = BaseRuntimeEvent


# --- 19 Concrete Event Models ---

class MissionEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.MISSION

class PlannerEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.PLANNER

class ExecutionEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.EXECUTION

class WorkerEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.WORKER

class ResourceEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.RESOURCE

class MemoryEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.MEMORY

class ReflectionEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.REFLECTION

class GovernanceEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.GOVERNANCE

class ValidationEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.VALIDATION

class ToolEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.TOOL

class StorageEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.STORAGE

class CostEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.COST

class SchedulerEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.SCHEDULER

class FailureEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.FAILURE

class RecoveryEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.RECOVERY

class HumanReviewEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.HUMAN_REVIEW

class TelemetryEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.TELEMETRY

class BenchmarkEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.BENCHMARK

class SystemEvent(BaseRuntimeEvent):
    category: EventCategory = EventCategory.SYSTEM


# --- Profiling, Metric & Health Data Models ---

class SpanProfile(BaseModel):
    span_id: str
    parent_span_id: Optional[str] = None
    operation: str
    component: str
    start_time: float
    end_time: float
    duration_ms: float
    status: str
    children: List[SpanProfile] = Field(default_factory=list)
    attributes: Dict[str, Any] = Field(default_factory=dict)


class FlameGraphNode(BaseModel):
    name: str
    value_ms: float
    children: List[FlameGraphNode] = Field(default_factory=list)
    component: str = "runtime"
    span_id: Optional[str] = None
    is_critical_path: bool = False


class MetricRecord(BaseModel):
    name: str
    value: float
    unit: str
    timestamp: float = Field(default_factory=time.time)
    labels: Dict[str, str] = Field(default_factory=dict)
    provenance_event_ids: List[str] = Field(default_factory=list)


class AnomalyReport(BaseModel):
    anomaly_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metric_name: str
    anomaly_type: str  # LATENCY_SPIKE, MEMORY_LEAK, RETRY_EXPLOSION, WORKER_STARVATION, COST_RUNAWAY
    severity: EventSeverity
    observed_value: float
    expected_mean: float
    z_score: float
    timestamp: float = Field(default_factory=time.time)
    details: str
    root_cause_hint: Optional[str] = None


class RuntimeHealthScore(BaseModel):
    overall_score: float  # [0.0, 1.0]
    is_healthy: bool
    component_scores: Dict[str, float]  # CPU, Memory, Queue, FailureRate, RetryRate, Planner
    active_anomalies: List[AnomalyReport] = Field(default_factory=list)
    active_workers_count: int
    queue_backlog: int
    evaluated_at: float = Field(default_factory=time.time)
    provenance: Dict[str, Any] = Field(default_factory=dict)


class MissionTimelineItem(BaseModel):
    event_id: str
    timestamp: float
    stage: str
    category: str
    event_type: str
    status: str
    duration_ms: float
    summary: str
    evidence: Dict[str, Any] = Field(default_factory=dict)
    event_hash: Optional[str] = None


class MissionSnapshotPayload(BaseModel):
    mission_id: str
    status: str
    created_at: float
    updated_at: float
    total_events: int
    total_duration_ms: float
    total_tokens_used: int
    total_cost_usd: float
    active_nodes_count: int
    completed_nodes_count: int
    failed_nodes_count: int
    retries_count: int
    timeline: List[MissionTimelineItem] = Field(default_factory=list)
    current_metrics: Dict[str, float] = Field(default_factory=dict)
