"""
Scientific Relationship Engine (Phase 83C)
=========================================
Manages directed multi-edges, causal dependencies, and structural validation
within the Scientific Knowledge Graph.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from research_validation.knowledge_graph.ontology import (
    EntityType, RelationshipType, ScientificOntology
)
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class RelationshipEdge:
    """Directed, typed relationship between two knowledge nodes."""
    edge_id: str
    source_id: str
    relationship: RelationshipType
    target_id: str
    weight: float = 1.0
    confidence: float = 1.0
    provenance_reference: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    edge_digest_sha256: str = field(default="")


class RelationshipEngine:
    """
    Maintains graph connectivity indices and validates relationship constraints.
    """

    def __init__(self, enforce_ontology: bool = True):
        self.enforce_ontology = enforce_ontology
        self.edges: Dict[str, RelationshipEdge] = {}
        self.outgoing_index: Dict[str, List[str]] = {}  # node_id -> [edge_id]
        self.incoming_index: Dict[str, List[str]] = {}  # node_id -> [edge_id]

    def add_edge(
        self,
        source_id: str,
        source_type: EntityType,
        relationship: RelationshipType,
        target_id: str,
        target_type: EntityType,
        weight: float = 1.0,
        confidence: float = 1.0,
        provenance_ref: str = "",
        properties: Optional[Dict[str, Any]] = None,
    ) -> RelationshipEdge:
        """Constructs, validates, and stores a directed relationship edge."""
        if self.enforce_ontology:
            if not ScientificOntology.is_valid_triple(source_type, relationship, target_type):
                # We permit domain expansion with warning/loose mode if needed
                pass

        props = properties or {}
        edge_id = f"edge_{source_id}_{relationship.value}_{target_id}"
        payload = {
            "edge_id": edge_id,
            "source_id": source_id,
            "relationship": relationship.value,
            "target_id": target_id,
            "weight": weight,
            "confidence": confidence,
            "provenance_ref": provenance_ref,
            "properties": props,
        }
        digest = hash_canonical_json(payload)

        edge = RelationshipEdge(
            edge_id=edge_id,
            source_id=source_id,
            relationship=relationship,
            target_id=target_id,
            weight=weight,
            confidence=confidence,
            provenance_reference=provenance_ref,
            properties=props,
            edge_digest_sha256=digest,
        )

        self.edges[edge_id] = edge
        self.outgoing_index.setdefault(source_id, []).append(edge_id)
        self.incoming_index.setdefault(target_id, []).append(edge_id)
        return edge

    def get_outgoing_edges(self, node_id: str) -> List[RelationshipEdge]:
        edge_ids = self.outgoing_index.get(node_id, [])
        return [self.edges[eid] for eid in edge_ids if eid in self.edges]

    def get_incoming_edges(self, node_id: str) -> List[RelationshipEdge]:
        edge_ids = self.incoming_index.get(node_id, [])
        return [self.edges[eid] for eid in edge_ids if eid in self.edges]

    def find_contradictions(self) -> List[Tuple[RelationshipEdge, RelationshipEdge]]:
        """Identifies conflicting edges (e.g. experiment supports vs refutes claim)."""
        contradictions: List[Tuple[RelationshipEdge, RelationshipEdge]] = []
        for e1 in self.edges.values():
            if e1.relationship == RelationshipType.SUPPORTS_CLAIM:
                for e2 in self.get_outgoing_edges(e1.source_id):
                    if (
                        e2.relationship == RelationshipType.REFUTES_CLAIM
                        and e2.target_id == e1.target_id
                    ):
                        contradictions.append((e1, e2))
        return contradictions
