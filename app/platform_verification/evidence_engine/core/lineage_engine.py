"""
Evidence Lineage Engine building directed provenance DAGs.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceLineageNode,
    LineageRelation,
)
from app.platform_verification.evidence_engine.domain.interfaces import ILineageEngine


class EvidenceLineageEngine(ILineageEngine):
    """Constructs and queries the complete provenance lineage DAG."""

    def __init__(self) -> None:
        self._nodes: Dict[str, EvidenceLineageNode] = {}

    def register_node(
        self, node_id: str, node_type: str, attributes: Optional[Dict[str, Any]] = None, checksum: str = ""
    ) -> EvidenceLineageNode:
        node = EvidenceLineageNode(
            node_id=node_id,
            node_type=node_type,
            attributes=attributes or {},
            checksum=checksum,
        )
        self._nodes[node_id] = node
        return node

    def link_nodes(self, parent_id: str, child_id: str, relation: str = "derived_from") -> None:
        if parent_id not in self._nodes or child_id not in self._nodes:
            raise KeyError(f"Both parent ({parent_id}) and child ({child_id}) must be registered before linking.")
        parent = self._nodes[parent_id]
        child = self._nodes[child_id]

        if child_id not in parent.children:
            parent.children.append(child_id)
        if parent_id not in child.parents:
            child.parents.append(parent_id)
            child.relations[parent_id] = relation

    def trace_lineage(self, node_id: str) -> Dict[str, Any]:
        if node_id not in self._nodes:
            raise KeyError(f"Node '{node_id}' not found in lineage graph.")

        visited: set[str] = set()
        ancestors: List[Dict[str, Any]] = []

        def _traverse_up(curr_id: str):
            if curr_id in visited:
                return
            visited.add(curr_id)
            node = self._nodes[curr_id]
            for p_id in node.parents:
                ancestors.append({
                    "parent_id": p_id,
                    "child_id": curr_id,
                    "relation": node.relations.get(p_id, "derived_from"),
                    "parent_type": self._nodes[p_id].node_type,
                })
                _traverse_up(p_id)

        _traverse_up(node_id)
        target = self._nodes[node_id]
        return {
            "target_node_id": node_id,
            "target_type": target.node_type,
            "ancestor_links": ancestors,
            "total_ancestors": len(visited) - 1,
        }
