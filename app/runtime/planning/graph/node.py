"""
Dynamic DAG Execution Node Schema & Lifecycle Model.

Defines production-grade DAG Node representation, execution statuses, dependency specifications,
cost/token economics, probabilistic confidence scores, and runtime metadata.
"""

from __future__ import annotations

import enum
import time
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class NodeStatus(str, enum.Enum):
    READY = "READY"
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    RETRYING = "RETRYING"
    MUTATED = "MUTATED"


class DependencyType(str, enum.Enum):
    HARD = "HARD"                  # Must succeed; failure blocks downstream
    SOFT = "SOFT"                  # Best effort; failure produces partial input
    OPTIONAL = "OPTIONAL"          # May be skipped if bypassed
    CONDITIONAL = "CONDITIONAL"    # Evaluates boolean runtime condition predicate
    RUNTIME = "RUNTIME"            # Dynamically discovered during execution
    HUMAN_APPROVAL = "HUMAN_APPROVAL"  # Requires explicit operator signoff


class DependencySpec(BaseModel):
    parent_node_id: str
    dependency_type: DependencyType = DependencyType.HARD
    condition_expr: Optional[str] = None
    is_satisfied: bool = False
    resolved_at: Optional[float] = None


class DAGNode(BaseModel):
    """Production-grade DAG Execution Node with complete provenance and economic tracking."""
    node_id: str = Field(default_factory=lambda: f"node-{uuid.uuid4().hex[:8]}")
    mission_id: str
    name: str
    task_type: str  # e.g., "OCR", "EXTRACTION", "VALIDATION", "SMT_PROOF", "REFLECTION"
    status: NodeStatus = NodeStatus.WAITING
    dependencies: List[DependencySpec] = Field(default_factory=list)
    priority: int = Field(default=50, ge=1, le=100)  # 1 = Highest, 100 = Lowest
    
    # Economics & Predictions
    estimated_cost_usd: float = 0.001
    estimated_tokens: int = 500
    estimated_runtime_ms: float = 200.0
    expected_utility: float = 0.85
    risk_score: float = 0.10
    confidence_score: float = 0.90
    
    # Worker Allocation
    assigned_worker: Optional[str] = None
    required_capabilities: List[str] = Field(default_factory=lambda: ["GENERAL"])
    
    # Execution Lifecycle
    retry_count: int = 0
    max_retries: int = 3
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    actual_runtime_ms: float = 0.0
    
    # Critical Path Method (CPM) Metrics
    earliest_start_ms: float = 0.0
    latest_start_ms: float = 0.0
    earliest_finish_ms: float = 0.0
    latest_finish_ms: float = 0.0
    total_slack_ms: float = 0.0
    is_critical_path: bool = False
    
    # Payload & Evidence
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    resource_usage: Dict[str, float] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def mark_running(self, worker_id: str) -> None:
        self.status = NodeStatus.RUNNING
        self.assigned_worker = worker_id
        self.start_time = time.time()

    def mark_completed(self, outputs: Optional[Dict[str, Any]] = None) -> None:
        self.status = NodeStatus.COMPLETED
        self.end_time = time.time()
        if self.start_time:
            self.actual_runtime_ms = max(0.1, (self.end_time - self.start_time) * 1000.0)
        if outputs:
            self.outputs.update(outputs)

    def mark_failed(self, error: str) -> None:
        self.status = NodeStatus.FAILED
        self.end_time = time.time()
        if self.start_time:
            self.actual_runtime_ms = max(0.1, (self.end_time - self.start_time) * 1000.0)
        self.error_message = error

    def mark_retrying(self) -> None:
        self.retry_count += 1
        self.status = NodeStatus.RETRYING
        self.start_time = None
        self.end_time = None

    def mark_mutated(self, reason: str) -> None:
        self.status = NodeStatus.MUTATED
        self.metadata["mutation_reason"] = reason

    def get_parent_ids(self) -> List[str]:
        return [d.parent_node_id for d in self.dependencies]

    def is_ready(self, completed_node_ids: set[str]) -> bool:
        """Evaluates whether all hard/soft dependencies are satisfied."""
        if self.status not in (NodeStatus.WAITING, NodeStatus.READY):
            return False
        for dep in self.dependencies:
            if dep.dependency_type == DependencyType.HARD and dep.parent_node_id not in completed_node_ids:
                return False
            elif dep.dependency_type == DependencyType.OPTIONAL:
                continue
        return True
