"""
Graph Query Engine for Phase 10 (AISLCOP).

Provides pre-planning query capabilities with cryptographically verified edge traversal.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.runtime.intelligence.knowledge.knowledge_graph import (
    AdaptiveKnowledgeGraph,
    GraphEdge,
    GraphNode,
)


class GraphQueryEngine:
    """
    Executes semantic and relationship queries over the adaptive knowledge graph.
    """

    def __init__(self, graph: AdaptiveKnowledgeGraph):
        self.graph = graph

    def find_strategies_for_domain(self, domain_label: str) -> List[Dict[str, Any]]:
        """Finds strategies linked to a domain or entity with supporting evidence."""
        results: List[Dict[str, Any]] = []
        for edge in self.graph._edges.values():
            if edge.relationship == "APPLIES_STRATEGY":
                source = self.graph.get_node(edge.source_id)
                target = self.graph.get_node(edge.target_id)
                if source and target and domain_label.lower() in source.label.lower():
                    results.append({
                        "domain": source.label,
                        "strategy_id": target.node_id,
                        "strategy_name": target.label,
                        "weight": edge.weight,
                        "evidence_hash": edge.evidence_hash,
                    })
        return results

    def trace_evidence_lineage(self, outcome_node_id: str) -> List[Dict[str, Any]]:
        """Backwards traversal from outcome node to find all supporting evidence nodes."""
        lineage: List[Dict[str, Any]] = []
        visited = set()
        queue = [outcome_node_id]

        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)

            node = self.graph.get_node(curr)
            if node and node.node_type == "EVIDENCE":
                lineage.append({
                    "node_id": node.node_id,
                    "label": node.label,
                    "properties": node.properties,
                })

            # Check incoming edges
            incoming_edge_ids = self.graph._reverse_adj.get(curr, [])
            for eid in incoming_edge_ids:
                edge = self.graph.get_edge(eid)
                if edge and edge.source_id not in visited:
                    queue.append(edge.source_id)

        return lineage
