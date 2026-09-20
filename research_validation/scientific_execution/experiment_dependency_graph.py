"""
Experiment Dependency Graph (Phase 82B.2)
=========================================
DAG representation for multi-stage scientific experiment pipelines:
Raw Dataset -> Preprocessing -> Benchmark -> Aggregation -> Visualization -> Publication Figure -> Research Report

Implements topological sorting, cycle detection, and cascade descendant
invalidation upon upstream modification or data perturbation.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from research_validation.provenance.hashing import hash_canonical_json


class PipelineStageType(str, Enum):
    RAW_DATASET = "RAW_DATASET"
    PREPROCESSING = "PREPROCESSING"
    BENCHMARK = "BENCHMARK"
    AGGREGATION = "AGGREGATION"
    VISUALIZATION = "VISUALIZATION"
    PUBLICATION_FIGURE = "PUBLICATION_FIGURE"
    RESEARCH_REPORT = "RESEARCH_REPORT"


class NodeState(str, Enum):
    PENDING = "PENDING"
    VALID = "VALID"
    STALE = "STALE"
    INVALIDATED = "INVALIDATED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class PipelineNode:
    node_id: str
    stage_type: PipelineStageType
    name: str
    parent_ids: Tuple[str, ...] = ()
    config: Dict[str, Any] = field(default_factory=dict)
    state: NodeState = NodeState.PENDING
    output_hash: Optional[str] = None
    last_executed_utc: Optional[str] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "stage_type": self.stage_type.value,
            "name": self.name,
            "parent_ids": list(self.parent_ids),
            "config": self.config,
            "state": self.state.value,
            "output_hash": self.output_hash,
            "last_executed_utc": self.last_executed_utc,
        }


class ExperimentDependencyGraph:
    """
    Manages experiment stage dependencies and cascade invalidation.
    """

    def __init__(self, graph_id: str = "pipeline_dag"):
        self.graph_id = graph_id
        self._nodes: Dict[str, PipelineNode] = {}
        self._children: Dict[str, Set[str]] = {}

    def add_node(
        self,
        node_id: str,
        stage_type: PipelineStageType,
        name: str,
        parent_ids: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> PipelineNode:
        """Add a stage node to the pipeline DAG."""
        parents = tuple(parent_ids or [])
        for pid in parents:
            if pid not in self._nodes:
                raise KeyError(f"Parent node '{pid}' not found in pipeline DAG.")

        node = PipelineNode(
            node_id=node_id,
            stage_type=stage_type,
            name=name,
            parent_ids=parents,
            config=config or {},
            state=NodeState.PENDING,
        )

        self._nodes[node_id] = node
        if node_id not in self._children:
            self._children[node_id] = set()

        for pid in parents:
            self._children[pid].add(node_id)

        # Check for cycles
        if self._has_cycle():
            del self._nodes[node_id]
            for pid in parents:
                self._children[pid].discard(node_id)
            raise ValueError(f"Adding node '{node_id}' would introduce a circular dependency.")

        return node

    def get_node(self, node_id: str) -> Optional[PipelineNode]:
        return self._nodes.get(node_id)

    @property
    def nodes(self) -> Dict[str, PipelineNode]:
        return dict(self._nodes)

    def topological_sort(self) -> List[str]:
        """Compute execution order using Kahn's algorithm."""
        in_degree = {nid: len(n.parent_ids) for nid, n in self._nodes.items()}
        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        ordered: List[str] = []

        while queue:
            curr = queue.pop(0)
            ordered.append(curr)
            for child_id in self._children.get(curr, set()):
                in_degree[child_id] -= 1
                if in_degree[child_id] == 0:
                    queue.append(child_id)

        if len(ordered) != len(self._nodes):
            raise ValueError("Cycle detected during topological sorting.")

        return ordered

    def update_node_output(self, node_id: str, output_hash: str) -> PipelineNode:
        """Mark a node as valid with its computed output hash."""
        node = self._nodes[node_id]
        now_str = datetime.now(timezone.utc).isoformat()
        updated = PipelineNode(
            node_id=node.node_id,
            stage_type=node.stage_type,
            name=node.name,
            parent_ids=node.parent_ids,
            config=node.config,
            state=NodeState.VALID,
            output_hash=output_hash,
            last_executed_utc=now_str,
        )
        self._nodes[node_id] = updated
        return updated

    def invalidate_node(self, node_id: str, reason: str = "Upstream modified") -> Set[str]:
        """
        Cascade-invalidate a node and all of its downstream descendants.
        Returns the set of all invalidated node IDs.
        """
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found.")

        invalidated: Set[str] = set()
        queue = [node_id]

        while queue:
            curr = queue.pop(0)
            if curr not in invalidated:
                invalidated.add(curr)
                node = self._nodes[curr]
                self._nodes[curr] = PipelineNode(
                    node_id=node.node_id,
                    stage_type=node.stage_type,
                    name=node.name,
                    parent_ids=node.parent_ids,
                    config=node.config,
                    state=NodeState.INVALIDATED,
                    output_hash=None,
                    last_executed_utc=node.last_executed_utc,
                )
                queue.extend(list(self._children.get(curr, set())))

        return invalidated

    def _has_cycle(self) -> bool:
        visited: Dict[str, int] = {k: 0 for k in self._nodes}

        def dfs(u: str) -> bool:
            visited[u] = 1
            for v in self._children.get(u, set()):
                if visited.get(v, 0) == 1:
                    return True
                if visited.get(v, 0) == 0 and dfs(v):
                    return True
            visited[u] = 2
            return False

        for n in self._nodes:
            if visited[n] == 0:
                if dfs(n):
                    return True
        return False
