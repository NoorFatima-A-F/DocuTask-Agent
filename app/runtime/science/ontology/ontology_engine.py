from __future__ import annotations
"""
Ontology Engine for Phase 13.12 Autonomous Scientific Discovery.
Manages dynamic semantic ontology expansion, concept taxonomy, and relationship graph.
"""


import logging
from app.core.security import sanitize_log_input
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
import uuid

from app.runtime.science.events.science_events import (
    ScienceEventBus,
    ScientificDomainEvent,
    ScientificEventType,
)

logger = logging.getLogger(__name__)


@dataclass
class OntologyConcept:
    """Represents a discovered or foundational semantic concept."""
    concept_id: str
    name: str
    domain: str
    definition: str
    synonyms: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.90
    discovered_by_hypothesis_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concept_id": self.concept_id,
            "name": self.name,
            "domain": self.domain,
            "definition": self.definition,
            "synonyms": self.synonyms,
            "attributes": self.attributes,
            "confidence": round(self.confidence, 4),
            "discovered_by_hypothesis_id": self.discovered_by_hypothesis_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class OntologyRelation:
    """Represents a semantic or causal relation between two concepts."""
    relation_id: str
    source_concept_id: str
    target_concept_id: str
    relation_type: str  # is_a, causes, optimizes, regulates, correlates_with, part_of, contradicts
    weight: float = 1.0
    evidence_ids: List[str] = field(default_factory=list)
    confidence: float = 0.85
    discovered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "relation_id": self.relation_id,
            "source_concept_id": self.source_concept_id,
            "target_concept_id": self.target_concept_id,
            "relation_type": self.relation_type,
            "weight": round(self.weight, 4),
            "evidence_ids": self.evidence_ids,
            "confidence": round(self.confidence, 4),
            "discovered_at": self.discovered_at.isoformat(),
        }


class OntologyEngine:
    """
    Autonomous Semantic Ontology Expansion Engine.
    Dynamically expands the platform's ontological graph with discovered scientific constructs.
    """

    def __init__(self, event_bus: Optional[ScienceEventBus] = None):
        self.event_bus = event_bus or ScienceEventBus()
        self.concepts: Dict[str, OntologyConcept] = {}
        self.relations: Dict[str, OntologyRelation] = {}
        self._initialize_foundational_ontology()

    def _initialize_foundational_ontology(self) -> None:
        """Seeds standard core enterprise & system cognition concepts."""
        seeds = [
            ("concept_agent_latency", "Agent Latency", "performance", "Turnaround response time of agent reasoning cycles"),
            ("concept_memory_footprint", "Memory Footprint", "resource", "RAM and context memory consumed by agent swarms"),
            ("concept_swarm_throughput", "Swarm Throughput", "throughput", "Completed autonomous operations per unit time"),
            ("concept_accuracy_rate", "Verification Accuracy", "quality", "Precision of verification checks across truth ledgers"),
            ("concept_governance_compliance", "Governance Compliance", "safety", "Adherence score against autonomous policy constraints"),
            ("concept_context_entropy", "Context Entropy", "cognition", "Information disorder and token drift in cognitive memory"),
        ]
        for cid, name, domain, definition in seeds:
            self.concepts[cid] = OntologyConcept(
                concept_id=cid,
                name=name,
                domain=domain,
                definition=definition,
                confidence=1.0,
            )

        # Seed foundational relations
        rel_seeds = [
            ("rel_mem_lat", "concept_memory_footprint", "concept_agent_latency", "correlates_with", 0.75),
            ("rel_entropy_acc", "concept_context_entropy", "concept_accuracy_rate", "regulates", 0.88),
            ("rel_lat_throughput", "concept_agent_latency", "concept_swarm_throughput", "causes", 0.92),
        ]
        for rid, src, tgt, rtype, conf in rel_seeds:
            self.relations[rid] = OntologyRelation(
                relation_id=rid,
                source_concept_id=src,
                target_concept_id=tgt,
                relation_type=rtype,
                confidence=conf,
            )

    def register_concept(
        self,
        name: str,
        domain: str,
        definition: str,
        synonyms: Optional[List[str]] = None,
        attributes: Optional[Dict[str, Any]] = None,
        confidence: float = 0.90,
        discovered_by_hypothesis_id: Optional[str] = None,
    ) -> OntologyConcept:
        """Registers or updates an ontological concept."""
        # Check if concept already exists by name
        for existing in self.concepts.values():
            if existing.name.lower() == name.lower() and existing.domain.lower() == domain.lower():
                existing.definition = definition
                if synonyms:
                    existing.synonyms = list(set(existing.synonyms + synonyms))
                if attributes:
                    existing.attributes.update(attributes)
                existing.confidence = max(existing.confidence, confidence)
                return existing

        concept_id = f"concept_{uuid.uuid4().hex[:8]}"
        concept = OntologyConcept(
            concept_id=concept_id,
            name=name,
            domain=domain,
            definition=definition,
            synonyms=synonyms or [],
            attributes=attributes or {},
            confidence=confidence,
            discovered_by_hypothesis_id=discovered_by_hypothesis_id,
        )
        self.concepts[concept_id] = concept

        self.event_bus.publish(
            ScientificDomainEvent(
                event_type=ScientificEventType.ONTOLOGY_EXPANDED,
                payload={
                    "action": "concept_registered",
                    "concept_id": concept_id,
                    "name": name,
                    "domain": domain,
                },
            )
        )
        logger.info("Registered ontology concept: %s (%s)", sanitize_log_input(name), sanitize_log_input(concept_id))
        return concept

    def link_concepts(
        self,
        source_concept_id: str,
        target_concept_id: str,
        relation_type: str,
        weight: float = 1.0,
        evidence_ids: Optional[List[str]] = None,
        confidence: float = 0.85,
    ) -> OntologyRelation:
        """Creates or updates a directed semantic edge between concepts."""
        if source_concept_id not in self.concepts:
            raise ValueError(f"Source concept {source_concept_id} not found in ontology")
        if target_concept_id not in self.concepts:
            raise ValueError(f"Target concept {target_concept_id} not found in ontology")

        # Check existing
        for rel in self.relations.values():
            if (
                rel.source_concept_id == source_concept_id
                and rel.target_concept_id == target_concept_id
                and rel.relation_type == relation_type
            ):
                rel.weight = weight
                rel.confidence = max(rel.confidence, confidence)
                if evidence_ids:
                    rel.evidence_ids = list(set(rel.evidence_ids + evidence_ids))
                return rel

        relation_id = f"rel_{uuid.uuid4().hex[:8]}"
        relation = OntologyRelation(
            relation_id=relation_id,
            source_concept_id=source_concept_id,
            target_concept_id=target_concept_id,
            relation_type=relation_type,
            weight=weight,
            evidence_ids=evidence_ids or [],
            confidence=confidence,
        )
        self.relations[relation_id] = relation

        self.event_bus.publish(
            ScientificDomainEvent(
                event_type=ScientificEventType.ONTOLOGY_EXPANDED,
                payload={
                    "action": "relation_created",
                    "relation_id": relation_id,
                    "source": source_concept_id,
                    "target": target_concept_id,
                    "type": relation_type,
                },
            )
        )
        return relation

    def get_concept(self, concept_id: str) -> Optional[OntologyConcept]:
        return self.concepts.get(concept_id)

    def list_concepts(self, domain: Optional[str] = None) -> List[OntologyConcept]:
        if domain:
            return [c for c in self.concepts.values() if c.domain.lower() == domain.lower()]
        return list(self.concepts.values())

    def list_relations(self) -> List[OntologyRelation]:
        return list(self.relations.values())

    def find_paths(
        self,
        source_concept_id: str,
        target_concept_id: str,
        max_depth: int = 4,
    ) -> List[List[Dict[str, Any]]]:
        """BFS path discovery between two concepts in the ontology graph."""
        if source_concept_id not in self.concepts or target_concept_id not in self.concepts:
            return []

        # Build adjacency
        adj: Dict[str, List[OntologyRelation]] = {}
        for r in self.relations.values():
            adj.setdefault(r.source_concept_id, []).append(r)

        paths: List[List[Dict[str, Any]]] = []
        queue: List[tuple[str, List[Dict[str, Any]], Set[str]]] = [(source_concept_id, [], {source_concept_id})]

        while queue:
            curr, path, visited = queue.pop(0)
            if curr == target_concept_id and path:
                paths.append(path)
                continue

            if len(path) >= max_depth:
                continue

            for edge in adj.get(curr, []):
                nxt = edge.target_concept_id
                if nxt not in visited:
                    edge_info = {
                        "from": curr,
                        "to": nxt,
                        "relation": edge.relation_type,
                        "weight": edge.weight,
                        "confidence": edge.confidence,
                    }
                    queue.append((nxt, path + [edge_info], visited | {nxt}))

        return paths

    def export_graph_summary(self) -> Dict[str, Any]:
        """Returns statistical overview and graph structure of ontology."""
        domains: Dict[str, int] = {}
        for c in self.concepts.values():
            domains[c.domain] = domains.get(c.domain, 0) + 1

        relation_types: Dict[str, int] = {}
        for r in self.relations.values():
            relation_types[r.relation_type] = relation_types.get(r.relation_type, 0) + 1

        return {
            "total_concepts": len(self.concepts),
            "total_relations": len(self.relations),
            "domains": domains,
            "relation_types": relation_types,
            "concepts": [c.to_dict() for c in self.concepts.values()],
            "relations": [r.to_dict() for r in self.relations.values()],
        }
