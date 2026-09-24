"""
Scientific Reasoning Engine (Phase 83C)
======================================
Derives logical inferences, synthesizes causal graphs, and resolves
contradictions across empirical findings in the Scientific Knowledge Graph.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from research_validation.knowledge_graph.knowledge_node import KnowledgeNode
from research_validation.knowledge_graph.ontology import EntityType, RelationshipType
from research_validation.knowledge_graph.relationship_engine import (
    RelationshipEngine
)


@dataclass(frozen=True)
class InferredRelationship:
    """A logically derived relation not directly observed."""
    source_id: str
    relationship: RelationshipType
    target_id: str
    rationale: str
    confidence: float
    derivation_rule: str


@dataclass(frozen=True)
class CausalGraphResult:
    """Extracted causal subgraph mapping interventions to empirical metrics."""
    interventions: List[str]
    mediators: List[str]
    outcomes: List[str]
    causal_edges: List[Tuple[str, str, float]]  # (source, target, strength)


class ScientificReasoningEngine:
    """
    Inference and causal discovery engine over the scientific knowledge graph.
    """

    def __init__(
        self,
        nodes: Dict[str, KnowledgeNode],
        rel_engine: RelationshipEngine,
    ):
        self.nodes = nodes
        self.rel_engine = rel_engine

    def infer_transitive_relations(self) -> List[InferredRelationship]:
        """Deduces transitive relationships (e.g., A CAUSES B and B CAUSES C => A CAUSES C)."""
        inferred: List[InferredRelationship] = []
        for edge1 in list(self.rel_engine.edges.values()):
            if edge1.relationship == RelationshipType.CAUSES:
                for edge2 in self.rel_engine.get_outgoing_edges(edge1.target_id):
                    if edge2.relationship == RelationshipType.CAUSES:
                        inferred.append(InferredRelationship(
                            source_id=edge1.source_id,
                            relationship=RelationshipType.CAUSES,
                            target_id=edge2.target_id,
                            rationale=f"Transitive deduction: {edge1.source_id} -> {edge1.target_id} -> {edge2.target_id}",
                            confidence=edge1.confidence * edge2.confidence * 0.9,
                            derivation_rule="TRANSITIVE_CAUSALITY",
                        ))
        return inferred

    def build_causal_graph(self) -> CausalGraphResult:
        """Constructs an directed causal network of parameters to measured metrics."""
        interventions: Set[str] = set()
        mediators: Set[str] = set()
        outcomes: Set[str] = set()
        causal_edges: List[Tuple[str, str, float]] = []

        for edge in self.rel_engine.edges.values():
            if edge.relationship in (RelationshipType.CAUSES, RelationshipType.CORRELATES_WITH):
                src_node = self.nodes.get(edge.source_id)
                tgt_node = self.nodes.get(edge.target_id)
                if src_node and tgt_node:
                    if src_node.entity_type in (EntityType.EXPERIMENT, EntityType.MODEL):
                        interventions.add(src_node.node_id)
                    elif src_node.entity_type == EntityType.METRIC:
                        mediators.add(src_node.node_id)

                    if tgt_node.entity_type == EntityType.METRIC:
                        outcomes.add(tgt_node.node_id)

                    causal_edges.append((src_node.node_id, tgt_node.node_id, edge.weight * edge.confidence))

        return CausalGraphResult(
            interventions=sorted(list(interventions)),
            mediators=sorted(list(mediators)),
            outcomes=sorted(list(outcomes)),
            causal_edges=causal_edges,
        )
