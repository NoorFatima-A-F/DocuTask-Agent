"""
Recovery Manager for Persistent Task Graph Intelligence.
Restores live DynamicTaskGraph instances from checkpoints, verifies cryptographic integrity,
and resumes execution cleanly from interrupted DAG nodes without repeating completed steps.
"""

from __future__ import annotations

import logging
from typing import Optional

from app.agents.planning.execution_plan import PlannedTask, TaskStatus
from app.agents.workflow.persistence.task_graph_repository import TaskGraphRepository
from app.agents.workflow.persistence.workflow_checkpoint import TaskGraphSnapshot
from app.agents.workflow.task_graph.dynamic_task_graph import (
    DynamicTaskGraph,
    GraphMutationEvent,
    NodeState,
)

logger = logging.getLogger(__name__)


class RecoveryManager:
    """Restores task graphs and orchestrates crash recovery."""

    def __init__(self, repository: TaskGraphRepository) -> None:
        self.repository = repository

    def restore_graph(
        self,
        snapshot: TaskGraphSnapshot,
        reset_interrupted_to_ready: bool = True,
    ) -> DynamicTaskGraph:
        """Reconstructs a fully functional DynamicTaskGraph from an immutable snapshot."""
        # 1. Integrity check
        if not snapshot.verify_integrity():
            raise ValueError(f"Snapshot {snapshot.snapshot_id} failed cryptographic integrity verification!")

        # 2. Instantiate graph
        graph = DynamicTaskGraph(plan_id=snapshot.plan_id)

        # 3. Restore nodes
        for tid, tdata in snapshot.nodes.items():
            task = PlannedTask(
                task_id=tdata["task_id"],
                name=tdata["name"],
                action=tdata["action"],
                assigned_agent=tdata.get("assigned_agent"),
                required_tools=list(tdata.get("required_tools", [])),
                dependencies=list(tdata.get("dependencies", [])),
                input_parameters=dict(tdata.get("input_parameters", {})),
                output_key=tdata.get("output_key", "result"),
                status=TaskStatus(tdata.get("status", "PENDING")),
                fallback_agent=tdata.get("fallback_agent"),
                fallback_tools=list(tdata.get("fallback_tools", [])),
                max_retries=tdata.get("max_retries", 2),
                timeout_seconds=tdata.get("timeout_seconds", 30.0),
                is_critical=tdata.get("is_critical", True),
                metadata=dict(tdata.get("metadata", {})),
            )
            graph._nodes[task.task_id] = task

        # 4. Restore states
        for tid, state_str in snapshot.states.items():
            state = NodeState(state_str)
            # If the node was interrupted in RUNNING state during a crash, reset to READY
            if reset_interrupted_to_ready and state == NodeState.RUNNING:
                state = NodeState.READY
                logger.info("Reset interrupted task %s from RUNNING to READY for recovery", tid)
            graph._states[tid] = state

        # 5. Restore outputs
        graph._outputs = dict(snapshot.outputs)

        # 6. Restore mutation history
        for m in snapshot.mutation_history:
            graph._history.append(
                GraphMutationEvent(
                    mutation_type=m["mutation_type"],
                    node_id=m["node_id"],
                    details=m["details"],
                )
            )

        graph.refresh_states()
        logger.info("Successfully recovered task graph %s from snapshot %s", graph.plan_id, snapshot.snapshot_id)
        return graph

    def recover_latest_plan(self, plan_id: str) -> Optional[DynamicTaskGraph]:
        """Loads latest checkpoint for a plan and restores it."""
        snapshot = self.repository.get_latest_by_plan(plan_id)
        if not snapshot:
            logger.warning("No checkpoint found for plan %s", plan_id)
            return None
        return self.restore_graph(snapshot)
