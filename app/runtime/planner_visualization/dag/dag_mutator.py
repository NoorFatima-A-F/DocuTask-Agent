"""
DAG Mutation Engine for Phase 13.2.
Performs dynamic in-flight DAG mutations, node splitting, recovery injections, and edge rewiring.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from app.runtime.planner_visualization.ui_models.models import (
    PlannerDAGNode,
    PlannerDAGEdge,
    TaskNodeType,
    TaskExecutionState,
)
from app.runtime.planner_visualization.dag.dag_engine import DAGBuilderEngine
from app.runtime.events.bus.event_bus import get_global_event_bus
from app.runtime.events.models.planner_event import PlannerEventFactory


class DAGMutationEngine:
    """
    Handles live DAG mutations triggered by task failures, confidence drops, or sub-task splitting.
    """

    def __init__(self, dag_builder: DAGBuilderEngine):
        self.dag_builder = dag_builder
        self.mutation_history: List[Dict[str, Any]] = []

    def split_node(self, target_node_id: str, num_splits: int = 2) -> Dict[str, Any]:
        """
        Splits a single heavy node into multiple parallel child tasks.
        """
        if target_node_id not in self.dag_builder.nodes:
            return {"status": "ERROR", "message": f"Node {target_node_id} not found"}

        original_node = self.dag_builder.nodes[target_node_id]
        original_node.state = TaskExecutionState.COMPLETED

        new_children = []
        for i in range(1, num_splits + 1):
            child_id = f"{target_node_id}_split_{i}"
            child_node = PlannerDAGNode(
                node_id=child_id,
                name=f"{original_node.name} (Part {i})",
                node_type=TaskNodeType.PARALLEL,
                state=TaskExecutionState.RUNNING,
                assigned_worker=f"worker-ocr-0{i}",
                parent_ids=[target_node_id],
                dependencies=[target_node_id],
                estimated_duration_ms=original_node.estimated_duration_ms / num_splits,
                confidence=0.99,
                event_id=f"evt-split-{child_id}",
                truth_ledger_hash=f"hash-{child_id}-split",
                replay_offset=len(self.dag_builder.nodes) + i,
            )
            self.dag_builder.nodes[child_id] = child_node
            self.dag_builder.edges.append(PlannerDAGEdge(source=target_node_id, target=child_id))
            new_children.append(child_id)

        self.dag_builder.version += 1
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mutation_type": "NODE_SPLIT",
            "target_node_id": target_node_id,
            "new_nodes_created": new_children,
            "version": self.dag_builder.version,
        }
        self.mutation_history.append(record)

        # Emit Replanned event
        event = PlannerEventFactory.replanned(
            mission_id=self.dag_builder.mission_id,
            reason=f"Split node {target_node_id} into {num_splits} parallel branches",
            mutated_nodes=[target_node_id] + new_children,
        )
        get_global_event_bus().publish_sync(event)

        return {"status": "SUCCESS", "mutation": record, "snapshot": self.dag_builder.get_snapshot()}

    def inject_recovery_node(self, failed_node_id: str, recovery_strategy: str = "FALLBACK_OCR") -> Dict[str, Any]:
        """
        Injects an adaptive recovery node when a task fails or invariant is violated.
        """
        if failed_node_id not in self.dag_builder.nodes:
            return {"status": "ERROR", "message": f"Node {failed_node_id} not found"}

        failed_node = self.dag_builder.nodes[failed_node_id]
        failed_node.state = TaskExecutionState.FAILED

        recovery_id = f"{failed_node_id}_recovery"
        recovery_node = PlannerDAGNode(
            node_id=recovery_id,
            name=f"Recovery [{recovery_strategy}]: {failed_node.name}",
            node_type=TaskNodeType.RECOVERY,
            state=TaskExecutionState.RUNNING,
            assigned_worker="worker-recovery-01",
            parent_ids=[failed_node_id],
            dependencies=[failed_node_id],
            estimated_duration_ms=failed_node.estimated_duration_ms * 1.2,
            confidence=0.999,
            event_id=f"evt-rec-{recovery_id}",
            truth_ledger_hash=f"hash-{recovery_id}-verified",
            replay_offset=len(self.dag_builder.nodes) + 1,
        )
        self.dag_builder.nodes[recovery_id] = recovery_node
        self.dag_builder.edges.append(PlannerDAGEdge(source=failed_node_id, target=recovery_id))

        self.dag_builder.version += 1
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mutation_type": "RECOVERY_INJECTION",
            "failed_node_id": failed_node_id,
            "recovery_node_id": recovery_id,
            "strategy": recovery_strategy,
            "version": self.dag_builder.version,
        }
        self.mutation_history.append(record)

        # Emit Replanned event
        event = PlannerEventFactory.replanned(
            mission_id=self.dag_builder.mission_id,
            reason=f"Injected recovery node for {failed_node_id} using {recovery_strategy}",
            mutated_nodes=[failed_node_id, recovery_id],
        )
        get_global_event_bus().publish_sync(event)

        return {"status": "SUCCESS", "mutation": record, "snapshot": self.dag_builder.get_snapshot()}
