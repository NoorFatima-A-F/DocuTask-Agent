"""
Runtime Dynamic DAG Mutator.

Enables live in-flight mutation of execution graphs (node insertion, subgraph replacement,
parallel splitting, recovery branch injection) with complete structural diffs and provenance.
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.runtime.planning.graph.dag import ExecutionDAG
from app.runtime.planning.graph.edge import DAGEdge, EdgeType
from app.runtime.planning.graph.node import DAGNode, NodeStatus


class GraphMutationRecord(BaseModel):
    """Immutable audit record of a dynamic runtime graph mutation."""
    mutation_id: str = Field(default_factory=lambda: f"mut-{uuid.uuid4().hex[:8]}")
    mission_id: str
    mutation_type: str  # INSERT_NODE, REMOVE_NODE, REPLACE_SUBGRAPH, INJECT_RECOVERY
    trigger_reason: str
    affected_node_ids: List[str]
    nodes_added_count: int
    nodes_removed_count: int
    edges_added_count: int
    edges_removed_count: int
    timestamp: float = Field(default_factory=time.time)
    diff_summary: Dict[str, Any] = Field(default_factory=dict)


class GraphMutator:
    """Performs transactional runtime graph mutations on an active ExecutionDAG."""

    @classmethod
    def insert_node_between(
        cls,
        dag: ExecutionDAG,
        new_node: DAGNode,
        parent_node_id: str,
        child_node_id: str,
        reason: str = "Dynamic runtime node insertion",
    ) -> GraphMutationRecord:
        """
        Inserts new_node between parent_node_id and child_node_id:
        Before: Parent -> Child
        After:  Parent -> NewNode -> Child
        """
        # Find existing edge
        existing_edge_id = None
        for eid, edge in dag.edges.items():
            if edge.source_node_id == parent_node_id and edge.target_node_id == child_node_id:
                existing_edge_id = eid
                break

        if existing_edge_id:
            dag.remove_edge(existing_edge_id)

        dag.add_node(new_node)
        dag.add_edge(DAGEdge(source_node_id=parent_node_id, target_node_id=new_node.node_id))
        dag.add_edge(DAGEdge(source_node_id=new_node.node_id, target_node_id=child_node_id))
        dag.generation += 1

        rec = GraphMutationRecord(
            mission_id=dag.mission_id,
            mutation_type="INSERT_NODE",
            trigger_reason=reason,
            affected_node_ids=[parent_node_id, new_node.node_id, child_node_id],
            nodes_added_count=1,
            nodes_removed_count=0,
            edges_added_count=2,
            edges_removed_count=1 if existing_edge_id else 0,
            diff_summary={
                "inserted_node": new_node.node_id,
                "parent": parent_node_id,
                "child": child_node_id,
            },
        )
        return rec

    @classmethod
    def inject_recovery_branch(
        cls,
        dag: ExecutionDAG,
        failed_node_id: str,
        recovery_nodes: List[DAGNode],
        resume_target_node_id: str,
        reason: str = "Failure-driven recovery branch injection",
    ) -> GraphMutationRecord:
        """
        Injects a recovery pipeline branching off a failed node to resume at downstream target:
        FailedNode -> Recovery_1 -> ... -> Recovery_k -> ResumeTarget
        """
        if failed_node_id in dag.nodes:
            dag.nodes[failed_node_id].mark_mutated(reason)

        prev_id = failed_node_id
        for r_node in recovery_nodes:
            dag.add_node(r_node)
            dag.add_edge(DAGEdge(source_node_id=prev_id, target_node_id=r_node.node_id))
            prev_id = r_node.node_id

        # Wire last recovery node to resume target
        if resume_target_node_id in dag.nodes:
            dag.add_edge(DAGEdge(source_node_id=prev_id, target_node_id=resume_target_node_id))

        dag.generation += 1

        rec = GraphMutationRecord(
            mission_id=dag.mission_id,
            mutation_type="INJECT_RECOVERY",
            trigger_reason=reason,
            affected_node_ids=[failed_node_id] + [n.node_id for n in recovery_nodes] + [resume_target_node_id],
            nodes_added_count=len(recovery_nodes),
            nodes_removed_count=0,
            edges_added_count=len(recovery_nodes) + 1,
            edges_removed_count=0,
            diff_summary={
                "failed_node": failed_node_id,
                "recovery_nodes": [n.node_id for n in recovery_nodes],
                "resumed_at": resume_target_node_id,
            },
        )
        return rec
