"""Mutable Execution DAG for DocuTask Autonomous Planning Platform.

Provides a fully dynamic, runtime-mutable Directed Acyclic Graph supporting node splitting,
node merging, node cloning, hot node replacement, branch insertion/pruning, and dependency rewiring.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class DAGNodeStatus(str, Enum):
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    MUTATED = "MUTATED"
    BYPASSED = "BYPASSED"


class DAGMutationType(str, Enum):
    NODE_SPLIT = "NODE_SPLIT"
    NODE_MERGE = "NODE_MERGE"
    NODE_CLONE = "NODE_CLONE"
    NODE_RETRY = "NODE_RETRY"
    NODE_REPLACE = "NODE_REPLACE"
    BRANCH_INSERT = "BRANCH_INSERT"
    BRANCH_PRUNE = "BRANCH_PRUNE"
    DEPENDENCY_REWIRE = "DEPENDENCY_REWIRE"


class DAGNode(BaseModel):
    """Execution unit within the dynamic DAG."""
    node_id: str = Field(default_factory=lambda: f"node_{uuid.uuid4().hex[:8]}")
    name: str
    capability_id: str
    provider: str
    status: DAGNodeStatus = DAGNodeStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    timeout_ms: float = 30000.0
    payload: Dict[str, Any] = Field(default_factory=dict)
    output: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DAGEdge(BaseModel):
    """Directed dependency edge between two DAG nodes."""
    edge_id: str = Field(default_factory=lambda: f"edge_{uuid.uuid4().hex[:8]}")
    source_id: str
    target_id: str
    condition: Optional[str] = None
    edge_type: str = "DATA"  # 'DATA', 'CONTROL'


class DAGMutationRecord(BaseModel):
    """Audit log entry capturing a structural DAG transformation at runtime."""
    mutation_id: str = Field(default_factory=lambda: f"mut_{uuid.uuid4().hex[:8]}")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mutation_type: DAGMutationType
    target_node_id: Optional[str] = None
    rationale: str
    diff_summary: str
    applied_by: str = "AutonomousPlanner"


class MutableExecutionDAG(BaseModel):
    """Stateful, mutable DAG representing the active mission execution graph."""
    dag_id: str = Field(default_factory=lambda: f"dag_{uuid.uuid4().hex[:10]}")
    mission_id: str
    strategy_id: str
    nodes: Dict[str, DAGNode] = Field(default_factory=dict)
    edges: List[DAGEdge] = Field(default_factory=list)
    mutation_history: List[DAGMutationRecord] = Field(default_factory=list)
    version: int = 1
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def add_node(self, node: DAGNode) -> None:
        self.nodes[node.node_id] = node

    def add_edge(self, source_id: str, target_id: str, condition: Optional[str] = None) -> DAGEdge:
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError(f"Invalid edge: source {source_id} or target {target_id} does not exist.")
        edge = DAGEdge(source_id=source_id, target_id=target_id, condition=condition)
        self.edges.append(edge)
        return edge

    def split_node(self, target_node_id: str, split_count: int, rationale: str) -> List[DAGNode]:
        """Splits a single node into N parallel sub-nodes and reconnects incoming/outgoing edges."""
        target = self.nodes.get(target_node_id)
        if not target:
            raise ValueError(f"Node {target_node_id} not found.")

        new_nodes: List[DAGNode] = []
        for i in range(split_count):
            sub_node = DAGNode(
                name=f"{target.name} [Shard {i+1}/{split_count}]",
                capability_id=target.capability_id,
                provider=target.provider,
                payload={"parent_node_id": target.node_id, "shard_index": i, "total_shards": split_count},
            )
            self.add_node(sub_node)
            new_nodes.append(sub_node)

        # Rewire incoming edges to all new shards
        incoming = [e for e in self.edges if e.target_id == target_node_id]
        for inc in incoming:
            for sub in new_nodes:
                self.add_edge(inc.source_id, sub.node_id, inc.condition)

        # Rewire outgoing edges: create a join node or wire shards directly to downstream
        outgoing = [e for e in self.edges if e.source_id == target_node_id]
        for out in outgoing:
            for sub in new_nodes:
                self.add_edge(sub.node_id, out.target_id, out.condition)

        # Remove old edges and mark target mutated
        self.edges = [e for e in self.edges if e.source_id != target_node_id and e.target_id != target_node_id]
        target.status = DAGNodeStatus.MUTATED

        self.version += 1
        self.mutation_history.append(
            DAGMutationRecord(
                mutation_type=DAGMutationType.NODE_SPLIT,
                target_node_id=target_node_id,
                rationale=rationale,
                diff_summary=f"Split node {target_node_id} into {split_count} parallel shards.",
            )
        )
        return new_nodes

    def merge_nodes(self, node_ids: List[str], merged_name: str, rationale: str) -> DAGNode:
        """Merges multiple nodes into a single consolidated execution node."""
        first_node = self.nodes.get(node_ids[0])
        merged = DAGNode(
            name=merged_name,
            capability_id=first_node.capability_id if first_node else "fast_rule_engine",
            provider=first_node.provider if first_node else "ast_validator",
            payload={"merged_node_ids": node_ids},
        )
        self.add_node(merged)

        # Collect incoming and outgoing
        incoming_sources = {e.source_id for e in self.edges if e.target_id in node_ids and e.source_id not in node_ids}
        outgoing_targets = {e.target_id for e in self.edges if e.source_id in node_ids and e.target_id not in node_ids}

        self.edges = [e for e in self.edges if e.source_id not in node_ids and e.target_id not in node_ids]

        for s_id in incoming_sources:
            self.add_edge(s_id, merged.node_id)
        for t_id in outgoing_targets:
            self.add_edge(merged.node_id, t_id)

        for nid in node_ids:
            if nid in self.nodes:
                self.nodes[nid].status = DAGNodeStatus.MUTATED

        self.version += 1
        self.mutation_history.append(
            DAGMutationRecord(
                mutation_type=DAGMutationType.NODE_MERGE,
                target_node_id=merged.node_id,
                rationale=rationale,
                diff_summary=f"Merged {len(node_ids)} nodes into single node {merged.node_id}.",
            )
        )
        return merged

    def clone_node(self, target_node_id: str, rationale: str) -> DAGNode:
        """Clones a node for redundant consensus or parallel verification."""
        target = self.nodes.get(target_node_id)
        if not target:
            raise ValueError(f"Node {target_node_id} not found.")

        clone = DAGNode(
            name=f"{target.name} [Consensus Clone]",
            capability_id=target.capability_id,
            provider=target.provider,
            payload=target.payload.copy(),
        )
        self.add_node(clone)

        # Mirror incoming edges
        for inc in [e for e in self.edges if e.target_id == target_node_id]:
            self.add_edge(inc.source_id, clone.node_id, inc.condition)

        self.version += 1
        self.mutation_history.append(
            DAGMutationRecord(
                mutation_type=DAGMutationType.NODE_CLONE,
                target_node_id=target_node_id,
                rationale=rationale,
                diff_summary=f"Cloned node {target_node_id} to {clone.node_id} for dual-verification.",
            )
        )
        return clone

    def replace_node_capability(
        self,
        target_node_id: str,
        new_capability_id: str,
        new_provider: str,
        rationale: str,
    ) -> DAGNode:
        """Hot-swaps capability provider on a node (e.g. OCR local -> OCR cloud on low confidence)."""
        target = self.nodes.get(target_node_id)
        if not target:
            raise ValueError(f"Node {target_node_id} not found.")

        old_cap = target.capability_id
        target.capability_id = new_capability_id
        target.provider = new_provider
        target.status = DAGNodeStatus.PENDING

        self.version += 1
        self.mutation_history.append(
            DAGMutationRecord(
                mutation_type=DAGMutationType.NODE_REPLACE,
                target_node_id=target_node_id,
                rationale=rationale,
                diff_summary=f"Replaced capability {old_cap} -> {new_capability_id} ({new_provider}).",
            )
        )
        return target

    def rewire_dependency(self, old_source_id: str, new_source_id: str, target_id: str, rationale: str) -> None:
        """Reroutes a dependency edge dynamically."""
        self.edges = [e for e in self.edges if not (e.source_id == old_source_id and e.target_id == target_id)]
        self.add_edge(new_source_id, target_id)
        self.version += 1
        self.mutation_history.append(
            DAGMutationRecord(
                mutation_type=DAGMutationType.DEPENDENCY_REWIRE,
                target_node_id=target_id,
                rationale=rationale,
                diff_summary=f"Rewired dependency: {old_source_id} -> {target_id} replaced with {new_source_id} -> {target_id}.",
            )
        )

    def get_prerequisites(self, node_id: str) -> List[str]:
        return [e.source_id for e in self.edges if e.target_id == node_id]

    def get_downstream(self, node_id: str) -> List[str]:
        return [e.target_id for e in self.edges if e.source_id == node_id]

    def validate_acyclic(self) -> bool:
        """Validates that the execution graph is strictly a Directed Acyclic Graph."""
        in_degree: Dict[str, int] = {k: 0 for k in self.nodes}
        adj: Dict[str, List[str]] = {k: [] for k in self.nodes}

        for edge in self.edges:
            adj[edge.source_id].append(edge.target_id)
            in_degree[edge.target_id] = in_degree.get(edge.target_id, 0) + 1

        queue = [k for k, deg in in_degree.items() if deg == 0]
        visited_count = 0

        while queue:
            curr = queue.pop(0)
            visited_count += 1
            for neighbor in adj.get(curr, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count == len(self.nodes)

    def get_topological_order(self) -> List[str]:
        in_degree: Dict[str, int] = {k: 0 for k in self.nodes}
        adj: Dict[str, List[str]] = {k: [] for k in self.nodes}

        for edge in self.edges:
            adj[edge.source_id].append(edge.target_id)
            in_degree[edge.target_id] = in_degree.get(edge.target_id, 0) + 1

        queue = [k for k, deg in in_degree.items() if deg == 0]
        order: List[str] = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for neighbor in adj.get(curr, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return order if len(order) == len(self.nodes) else list(self.nodes.keys())
