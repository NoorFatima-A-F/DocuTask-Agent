"""Runtime Provenance Graph (Evidence DAG) and Traversal Engine.

Constructs full bidirectional causality graphs connecting document raw inputs,
planner decisions, tool traces, extracted entities, validation checks, and final stores.
"""

from __future__ import annotations

import collections
import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class ProvenanceNode:
    node_id: str
    node_type: str  # INPUT, PLAN, TOOL, ARTIFACT, VALIDATION, OUTPUT
    label: str
    data_digest: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    parents: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "label": self.label,
            "data_digest": self.data_digest,
            "metadata": self.metadata,
            "parents": self.parents,
            "children": self.children,
        }


@dataclass
class LineagePath:
    path_nodes: List[str]
    total_latency_ms: float
    total_cost_usd: float
    confidence_product: float


class ProvenanceDAGBuilder:
    def __init__(self, dag_id: str = "runtime-provenance-dag"):
        self.dag_id = dag_id
        self._nodes: Dict[str, ProvenanceNode] = {}

    def add_node(
        self,
        node_id: str,
        node_type: str,
        label: str,
        data_digest: str,
        metadata: Optional[Dict[str, Any]] = None,
        parent_ids: Optional[List[str]] = None,
    ) -> ProvenanceNode:
        parents = parent_ids or []
        node = ProvenanceNode(
            node_id=node_id,
            node_type=node_type,
            label=label,
            data_digest=data_digest,
            metadata=metadata or {},
            parents=list(parents),
            children=[],
        )
        self._nodes[node_id] = node

        # Link parent's children
        for pid in parents:
            if pid in self._nodes and node_id not in self._nodes[pid].children:
                self._nodes[pid].children.append(node_id)

        return node

    def get_node(self, node_id: str) -> Optional[ProvenanceNode]:
        return self._nodes.get(node_id)

    def list_nodes(self) -> List[ProvenanceNode]:
        return list(self._nodes.values())

    def count(self) -> int:
        return len(self._nodes)

    def clear(self) -> None:
        self._nodes.clear()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dag_id": self.dag_id,
            "node_count": len(self._nodes),
            "nodes": [n.to_dict() for n in self._nodes.values()],
        }


class TraversalEngine:
    @staticmethod
    def trace_backward_lineage(dag: ProvenanceDAGBuilder, target_node_id: str) -> List[ProvenanceNode]:
        """Finds all ancestor nodes that influenced the target node (Root-cause attribution)."""
        visited: Set[str] = set()
        queue = collections.deque([target_node_id])
        ancestors: List[ProvenanceNode] = []

        while queue:
            curr_id = queue.popleft()
            if curr_id in visited:
                continue
            visited.add(curr_id)
            node = dag.get_node(curr_id)
            if node:
                ancestors.append(node)
                for pid in node.parents:
                    if pid not in visited:
                        queue.append(pid)

        return ancestors

    @staticmethod
    def trace_forward_impact(dag: ProvenanceDAGBuilder, source_node_id: str) -> List[ProvenanceNode]:
        """Finds all descendant nodes affected by this source node (Impact analysis)."""
        visited: Set[str] = set()
        queue = collections.deque([source_node_id])
        descendants: List[ProvenanceNode] = []

        while queue:
            curr_id = queue.popleft()
            if curr_id in visited:
                continue
            visited.add(curr_id)
            node = dag.get_node(curr_id)
            if node:
                descendants.append(node)
                for cid in node.children:
                    if cid not in visited:
                        queue.append(cid)

        return descendants


global_provenance_dag = ProvenanceDAGBuilder()
