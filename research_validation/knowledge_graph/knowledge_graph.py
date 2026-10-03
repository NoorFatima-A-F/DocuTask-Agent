"""
Scientific Knowledge Graph (Phase 83C)
=====================================
Unified master knowledge graph integrating entities, relationships,
semantic query engine, and deductive reasoning.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from research_validation.knowledge_graph.ontology import EntityType, RelationshipType
from research_validation.knowledge_graph.knowledge_node import (
    KnowledgeNode, create_node
)
from research_validation.knowledge_graph.relationship_engine import (
    RelationshipEdge, RelationshipEngine
)
from research_validation.knowledge_graph.semantic_query import SemanticQueryEngine
from research_validation.knowledge_graph.reasoning_engine import (
    ScientificReasoningEngine
)
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class KnowledgeGraphSnapshot:
    """Immutable, hash-sealed snapshot of the complete knowledge graph."""
    node_count: int
    edge_count: int
    root_digest_sha256: str
    timestamp_utc: str
    summary_by_type: Dict[str, int]


class ScientificKnowledgeGraph:
    """
    Master repository for all scientific entities, relationships,
    and empirical evidence in the autonomous research platform.
    """

    def __init__(self, enforce_ontology: bool = True):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.rel_engine = RelationshipEngine(enforce_ontology=enforce_ontology)
        self.query_engine = SemanticQueryEngine(self.nodes, self.rel_engine)
        self.reasoning_engine = ScientificReasoningEngine(self.nodes, self.rel_engine)

    def add_node(
        self,
        node_id: str,
        entity_type: EntityType,
        name: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> KnowledgeNode:
        """Adds a node to the knowledge graph."""
        node = create_node(node_id, entity_type, name, properties)
        self.nodes[node_id] = node
        return node

    def add_relationship(
        self,
        source_id: str,
        relationship: RelationshipType,
        target_id: str,
        weight: float = 1.0,
        confidence: float = 1.0,
        provenance_ref: str = "",
        properties: Optional[Dict[str, Any]] = None,
    ) -> RelationshipEdge:
        """Connects two existing nodes via a typed relationship edge."""
        src_node = self.nodes.get(source_id)
        tgt_node = self.nodes.get(target_id)
        if not src_node:
            raise KeyError(f"Source node '{source_id}' does not exist in knowledge graph.")
        if not tgt_node:
            raise KeyError(f"Target node '{target_id}' does not exist in knowledge graph.")

        return self.rel_engine.add_edge(
            source_id=source_id,
            source_type=src_node.entity_type,
            relationship=relationship,
            target_id=target_id,
            target_type=tgt_node.entity_type,
            weight=weight,
            confidence=confidence,
            provenance_ref=provenance_ref,
            properties=properties,
        )

    def get_snapshot(self) -> KnowledgeGraphSnapshot:
        """Generates a cryptographically sealed snapshot of current graph state."""
        counts: Dict[str, int] = {}
        for n in self.nodes.values():
            counts[n.entity_type.value] = counts.get(n.entity_type.value, 0) + 1

        payload = {
            "nodes": {nid: n.node_digest_sha256 for nid, n in sorted(self.nodes.items())},
            "edges": {eid: e.edge_digest_sha256 for eid, e in sorted(self.rel_engine.edges.items())},
        }
        root_digest = hash_canonical_json(payload)

        return KnowledgeGraphSnapshot(
            node_count=len(self.nodes),
            edge_count=len(self.rel_engine.edges),
            root_digest_sha256=root_digest,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            summary_by_type=counts,
        )

    def export_dot(self) -> str:
        """Exports graph to Graphviz DOT format for publication visualization."""
        lines = ["digraph ScientificKnowledgeGraph {", '  rankdir="LR";', '  node [shape="box", style="rounded,filled", fontname="Helvetica"];']
        
        color_map = {
            EntityType.EXPERIMENT: "#D0E1FD",
            EntityType.DATASET: "#D1FADF",
            EntityType.METRIC: "#FEF0C7",
            EntityType.MODEL: "#FCE7F6",
            EntityType.ENVIRONMENT: "#EAECF0",
            EntityType.HYPOTHESIS: "#E0EAFF",
            EntityType.CLAIM: "#FEE4E2",
        }

        for node in self.nodes.values():
            color = color_map.get(node.entity_type, "#FFFFFF")
            lines.append(f'  "{node.node_id}" [label="{node.name}\\n({node.entity_type.value})", fillcolor="{color}"];')

        for edge in self.rel_engine.edges.values():
            lines.append(f'  "{edge.source_id}" -> "{edge.target_id}" [label="{edge.relationship.value}", fontsize="9"];')

        lines.append("}")
        return "\n".join(lines)
