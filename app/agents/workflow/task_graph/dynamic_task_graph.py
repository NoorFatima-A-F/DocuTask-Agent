"""Dynamic Task Graph Runtime for Autonomous Agent Operating System.

Provides a live, mutable directed acyclic graph (DAG) capable of runtime state
transitions, topological analysis, dynamic concurrency resolution, and mutation.
"""

from __future__ import annotations

import copy
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from app.agents.planning.execution_plan import ExecutionPlan, PlannedTask, TaskStatus

logger = logging.getLogger(__name__)


class NodeState(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    MUTATED = "MUTATED"
    SKIPPED = "SKIPPED"


@dataclass
class GraphMutationEvent:
    """Audit record of a dynamic change in the task graph."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    mutation_type: str = ""  # "NODE_INSERTED", "NODE_REPLACED", "EDGE_REROUTED", "NODE_SKIPPED"
    node_id: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


class DynamicTaskGraph:
    """Mutable DAG managing runtime task lifecycles, dependencies, and execution waves."""

    def __init__(self, plan_id: str = "") -> None:
        self.plan_id = plan_id
        self._nodes: Dict[str, PlannedTask] = {}
        self._states: Dict[str, NodeState] = {}
        self._outputs: Dict[str, Any] = {}
        self._history: List[GraphMutationEvent] = []

    @classmethod
    def from_execution_plan(cls, plan: ExecutionPlan) -> DynamicTaskGraph:
        """Construct a live graph from an ExecutionPlan."""
        graph = cls(plan_id=plan.plan_id)
        for task in plan.tasks:
            graph.add_task(task)
        graph.refresh_states()
        return graph

    def add_task(self, task: PlannedTask) -> None:
        """Add a new task node to the graph and initialize its state."""
        if task.task_id in self._nodes:
            raise ValueError(f"Task node {task.task_id} already exists in graph")
        self._nodes[task.task_id] = copy.deepcopy(task)
        self._states[task.task_id] = NodeState.PENDING
        self._validate_acyclic()

    def get_task(self, task_id: str) -> Optional[PlannedTask]:
        return self._nodes.get(task_id)

    def get_state(self, task_id: str) -> NodeState:
        if task_id not in self._states:
            raise KeyError(f"Task {task_id} not in graph")
        return self._states[task_id]

    def set_state(self, task_id: str, state: NodeState | str) -> None:
        if task_id not in self._states:
            raise KeyError(f"Task {task_id} not in graph")
        node_state = state if isinstance(state, NodeState) else NodeState(str(state).upper())
        old_state = self._states[task_id]
        self._states[task_id] = node_state
        self._nodes[task_id].status = TaskStatus(node_state.value) if node_state.value in TaskStatus.__members__ else TaskStatus.PENDING
        logger.debug("Task %s transitioned: %s -> %s", task_id, old_state, node_state)
        self.refresh_states()

    def record_output(self, task_id: str, output: Any) -> None:
        self._outputs[task_id] = output
        self.set_state(task_id, NodeState.COMPLETED)

    def get_output(self, task_id: str) -> Any:
        return self._outputs.get(task_id)

    def get_all_outputs(self) -> Dict[str, Any]:
        return dict(self._outputs)

    def refresh_states(self) -> None:
        """Evaluate dependencies and promote PENDING to READY or demote READY to PENDING if dependencies changed."""
        completed_nodes = {tid for tid, s in self._states.items() if s == NodeState.COMPLETED}
        skipped_nodes = {tid for tid, s in self._states.items() if s == NodeState.SKIPPED}
        resolved = completed_nodes | skipped_nodes

        for tid, node in self._nodes.items():
            current_state = self._states[tid]
            all_deps_resolved = all(dep in resolved for dep in node.dependencies)

            if current_state == NodeState.PENDING and all_deps_resolved:
                self._states[tid] = NodeState.READY
                node.status = TaskStatus.READY
            elif current_state == NodeState.READY and not all_deps_resolved:
                self._states[tid] = NodeState.PENDING
                node.status = TaskStatus.PENDING

    def get_ready_tasks(self) -> List[PlannedTask]:
        """Return all tasks currently in READY state that can execute immediately."""
        self.refresh_states()
        return [self._nodes[tid] for tid, state in self._states.items() if state == NodeState.READY]

    def is_completed(self) -> bool:
        """Check if all tasks in the graph have reached terminal states."""
        terminal_states = {NodeState.COMPLETED, NodeState.SKIPPED}
        return all(state in terminal_states for state in self._states.values())

    def has_failures(self) -> bool:
        return any(state == NodeState.FAILED for state in self._states.values())

    def get_failed_tasks(self) -> List[PlannedTask]:
        return [self._nodes[tid] for tid, state in self._states.items() if state == NodeState.FAILED]

    def get_downstream_dependents(self, task_id: str) -> List[PlannedTask]:
        """Find all nodes that directly depend on the given task_id."""
        return [t for t in self._nodes.values() if task_id in t.dependencies]

    def record_mutation(self, mutation_type: str, node_id: str, details: Dict[str, Any]) -> None:
        self._history.append(
            GraphMutationEvent(
                mutation_type=mutation_type,
                node_id=node_id,
                details=details,
            )
        )

    def mutate(self, mutation_type: str, node_id: str, details: Dict[str, Any]) -> None:
        """Alias for record_mutation."""
        self.record_mutation(mutation_type=mutation_type, node_id=node_id, details=details)

    def get_mutation_history(self) -> List[GraphMutationEvent]:
        return list(self._history)

    def _validate_acyclic(self) -> None:
        """Validates that the graph is free of cycles."""
        in_degree: Dict[str, int] = {tid: 0 for tid in self._nodes}
        adj: Dict[str, List[str]] = {tid: [] for tid in self._nodes}

        for tid, task in self._nodes.items():
            for dep in task.dependencies:
                if dep in self._nodes:
                    adj[dep].append(tid)
                    in_degree[tid] += 1

        queue = [tid for tid, deg in in_degree.items() if deg == 0]
        visited_count = 0

        while queue:
            curr = queue.pop(0)
            visited_count += 1
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if visited_count < len(self._nodes):
            raise ValueError("Cycle detected in DynamicTaskGraph")
