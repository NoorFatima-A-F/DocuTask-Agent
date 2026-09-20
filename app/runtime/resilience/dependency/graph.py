"""
DocuTask Agent - Dynamic Runtime Dependency Graph
Phase 12: Autonomous Production Reliability & Operational Resilience (APRCORP+)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Any, Optional


@dataclass
class DependencyNode:
    id: str
    name: str
    type: str  # "SERVICE", "DATASTORE", "MODEL_PROVIDER", "PIPELINE_TASK"
    criticality: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    redundancy_level: int = 2
    dependencies: List[str] = field(default_factory=list)  # IDs of nodes this node depends on
    dependents: List[str] = field(default_factory=list)    # IDs of nodes that depend on this node


class DependencyGraph:
    """
    Dynamic Runtime Dependency Graph.
    Tracks topological relationships between micro-engines, external providers,
    datashards, and DAG tasks.
    """

    def __init__(self):
        self._nodes: Dict[str, DependencyNode] = {}
        self._seed_default_topology()

    def _seed_default_topology(self) -> None:
        """Seeds the standard platform dependency topology."""
        nodes = [
            DependencyNode("gemini-api", "Google Gemini API Gateway", "MODEL_PROVIDER", "CRITICAL", redundancy_level=2),
            DependencyNode("ocr-engine", "Document OCR Tesseract Engine", "SERVICE", "HIGH", redundancy_level=3),
            DependencyNode("redis-cache", "Redis Fast KV State Store", "DATASTORE", "HIGH", redundancy_level=3),
            DependencyNode("memory-graph", "Episodic Causal Memory", "DATASTORE", "HIGH", redundancy_level=2),
            DependencyNode("truth-ledger", "Truth & Proof Ledger", "DATASTORE", "CRITICAL", redundancy_level=3),
            DependencyNode("evidence-store", "Cryptographic Evidence Store", "DATASTORE", "CRITICAL", redundancy_level=3),
            DependencyNode("policy-engine", "Dynamic Sandbox & Policy", "SERVICE", "MEDIUM", redundancy_level=2),
            DependencyNode("dag-workers", "DAG Worker Subsystems", "SERVICE", "CRITICAL", redundancy_level=4),
            DependencyNode("planner-engine", "Autonomous Planner Engine", "SERVICE", "CRITICAL", redundancy_level=2),
        ]

        # Add nodes
        for n in nodes:
            self._nodes[n.id] = n

        # Add relationships
        self._add_edge("planner-engine", "dag-workers")
        self._add_edge("planner-engine", "truth-ledger")
        self._add_edge("dag-workers", "gemini-api")
        self._add_edge("dag-workers", "ocr-engine")
        self._add_edge("dag-workers", "redis-cache")
        self._add_edge("dag-workers", "memory-graph")
        self._add_edge("dag-workers", "evidence-store")
        self._add_edge("dag-workers", "policy-engine")

    def _add_edge(self, source_id: str, target_id: str) -> None:
        """source depends on target"""
        if source_id in self._nodes and target_id in self._nodes:
            if target_id not in self._nodes[source_id].dependencies:
                self._nodes[source_id].dependencies.append(target_id)
            if source_id not in self._nodes[target_id].dependents:
                self._nodes[target_id].dependents.append(source_id)

    def get_node(self, node_id: str) -> Optional[DependencyNode]:
        return self._nodes.get(node_id)

    def list_nodes(self) -> List[DependencyNode]:
        return list(self._nodes.values())

    def get_upstream_dependencies(self, node_id: str) -> List[str]:
        """Returns all upstream dependencies (transitive closure)."""
        visited: Set[str] = set()
        stack = [node_id]

        while stack:
            curr = stack.pop()
            if curr not in self._nodes:
                continue
            for dep in self._nodes[curr].dependencies:
                if dep not in visited:
                    visited.add(dep)
                    stack.append(dep)

        return list(visited)

    def get_downstream_impacted(self, node_id: str) -> List[str]:
        """Returns all downstream dependents affected if node fails (transitive closure)."""
        visited: Set[str] = set()
        stack = [node_id]

        while stack:
            curr = stack.pop()
            if curr not in self._nodes:
                continue
            for dep in self._nodes[curr].dependents:
                if dep not in visited:
                    visited.add(dep)
                    stack.append(dep)

        return list(visited)


# Global singleton instance
dependency_graph = DependencyGraph()
