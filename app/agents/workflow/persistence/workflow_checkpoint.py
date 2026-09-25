"""
Workflow Checkpoint Data Model for Persistent Task Graph Intelligence.
Provides immutable, serializable, and cryptographically verified snapshots of running task graphs.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID, uuid4

from app.agents.planning.execution_plan import TaskStatus
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph


@dataclass
class TaskGraphSnapshot:
    """Immutable serialized snapshot of a DynamicTaskGraph at a specific execution step."""

    snapshot_id: UUID = field(default_factory=uuid4)
    plan_id: str = ""
    session_id: str = ""
    step_index: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    nodes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    states: Dict[str, str] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    mutation_history: List[Dict[str, Any]] = field(default_factory=list)
    state_hash: str = ""

    def compute_hash(self) -> str:
        """Calculates SHA-256 hash over nodes, states, and outputs to verify integrity."""
        hasher = hashlib.sha256()
        hasher.update(self.plan_id.encode("utf-8"))
        hasher.update(str(self.step_index).encode("utf-8"))
        hasher.update(json.dumps(self.states, sort_keys=True).encode("utf-8"))
        hasher.update(json.dumps(self.nodes, sort_keys=True).encode("utf-8"))
        hasher.update(json.dumps(self.outputs, sort_keys=True, default=str).encode("utf-8"))
        return hasher.hexdigest()

    def verify_integrity(self) -> bool:
        """Validates that state_hash matches computed hash."""
        return self.state_hash == self.compute_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": str(self.snapshot_id),
            "plan_id": self.plan_id,
            "session_id": self.session_id,
            "step_index": self.step_index,
            "created_at": self.created_at.isoformat(),
            "nodes": self.nodes,
            "states": self.states,
            "outputs": self.outputs,
            "mutation_history": self.mutation_history,
            "state_hash": self.state_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TaskGraphSnapshot:
        return cls(
            snapshot_id=UUID(data["snapshot_id"]),
            plan_id=data["plan_id"],
            session_id=data.get("session_id", ""),
            step_index=data.get("step_index", 0),
            created_at=datetime.fromisoformat(data["created_at"]),
            nodes=data.get("nodes", {}),
            states=data.get("states", {}),
            outputs=data.get("outputs", {}),
            mutation_history=data.get("mutation_history", []),
            state_hash=data.get("state_hash", ""),
        )

    @classmethod
    def create(
        cls,
        graph: DynamicTaskGraph,
        session_id: str = "",
        step_index: int = 0,
    ) -> TaskGraphSnapshot:
        """Factory creating a cryptographically signed snapshot from a live DynamicTaskGraph."""
        serialized_nodes = {}
        for tid, task in graph._nodes.items():
            serialized_nodes[tid] = {
                "task_id": task.task_id,
                "name": task.name,
                "action": task.action,
                "assigned_agent": task.assigned_agent,
                "required_tools": list(task.required_tools),
                "dependencies": list(task.dependencies),
                "input_parameters": dict(task.input_parameters),
                "output_key": task.output_key,
                "status": task.status.value if isinstance(task.status, TaskStatus) else str(task.status),
                "fallback_agent": task.fallback_agent,
                "fallback_tools": list(task.fallback_tools),
                "max_retries": task.max_retries,
                "timeout_seconds": task.timeout_seconds,
                "is_critical": task.is_critical,
                "metadata": dict(task.metadata),
            }

        serialized_states = {tid: s.value for tid, s in graph._states.items()}
        serialized_mutations = [
            {
                "timestamp": m.timestamp.isoformat(),
                "mutation_type": m.mutation_type,
                "node_id": m.node_id,
                "details": m.details,
            }
            for m in graph._history
        ]

        snapshot = cls(
            plan_id=graph.plan_id,
            session_id=session_id,
            step_index=step_index,
            nodes=serialized_nodes,
            states=serialized_states,
            outputs=copy.deepcopy(graph._outputs),
            mutation_history=serialized_mutations,
        )
        snapshot.state_hash = snapshot.compute_hash()
        return snapshot
