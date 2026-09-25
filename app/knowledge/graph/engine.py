"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Enterprise Knowledge Graph.
Manages enterprise entities (Person, Company, Contract, Invoice, Policy, Department) and directed semantic relationships.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from app.knowledge.core.models import KnowledgeRelationship

logger = logging.getLogger(__name__)


class GraphEntity(BaseModel):
    """Node entity in the enterprise knowledge graph."""
    id: str
    entity_type: str  # Person, Company, Contract, Invoice, Policy, Project, Department
    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeGraphEngine:
    """
    In-memory graph database engine supporting entity-relationship indexing,
    neighborhood traversals, and multi-hop graph reasoning.
    """

    def __init__(self):
        self._entities: Dict[str, GraphEntity] = {}
        self._relations: Dict[str, KnowledgeRelationship] = {}
        self._adjacency: Dict[str, List[str]] = {}  # source_id -> [relation_id, ...]
        self._reverse_adj: Dict[str, List[str]] = {} # target_id -> [relation_id, ...]

    def add_entity(
        self,
        entity_id: str,
        entity_type: str,
        name: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> GraphEntity:
        """Upserts an entity node in the graph."""
        entity = GraphEntity(
            id=entity_id,
            entity_type=entity_type,
            name=name,
            properties=properties or {},
        )
        self._entities[entity_id] = entity
        if entity_id not in self._adjacency:
            self._adjacency[entity_id] = []
        if entity_id not in self._reverse_adj:
            self._reverse_adj[entity_id] = []
        return entity

    def add_relation(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        properties: Optional[Dict[str, Any]] = None,
        confidence: float = 1.0,
    ) -> KnowledgeRelationship:
        """Adds a directed relationship edge between two entities."""
        import uuid
        rel_id = f"krel-{uuid.uuid4().hex[:8]}"
        rel = KnowledgeRelationship(
            id=rel_id,
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            properties=properties or {},
            confidence=confidence,
        )
        self._relations[rel_id] = rel

        if source_id not in self._adjacency:
            self._adjacency[source_id] = []
        self._adjacency[source_id].append(rel_id)

        if target_id not in self._reverse_adj:
            self._reverse_adj[target_id] = []
        self._reverse_adj[target_id].append(rel_id)

        return rel

    def get_entity(self, entity_id: str) -> Optional[GraphEntity]:
        """Retrieves an entity by ID."""
        return self._entities.get(entity_id)

    def get_neighbors(
        self,
        entity_id: str,
        relation_type: Optional[str] = None,
        direction: str = "outgoing",  # outgoing, incoming, both
    ) -> List[Tuple[KnowledgeRelationship, GraphEntity]]:
        """
        Traverses adjacent nodes connected by matching relation types.
        """
        results: List[Tuple[KnowledgeRelationship, GraphEntity]] = []

        # Outgoing
        if direction in ("outgoing", "both") and entity_id in self._adjacency:
            for rel_id in self._adjacency[entity_id]:
                rel = self._relations[rel_id]
                if relation_type is None or rel.relation_type == relation_type:
                    target = self._entities.get(rel.target_id)
                    if target:
                        results.append((rel, target))

        # Incoming
        if direction in ("incoming", "both") and entity_id in self._reverse_adj:
            for rel_id in self._reverse_adj[entity_id]:
                rel = self._relations[rel_id]
                if relation_type is None or rel.relation_type == relation_type:
                    src = self._entities.get(rel.source_id)
                    if src:
                        results.append((rel, src))

        return results

    def find_path(
        self,
        start_id: str,
        end_id: str,
        max_depth: int = 4,
    ) -> Optional[List[str]]:
        """
        Breadth-First Search (BFS) for shortest path between two graph entities.
        """
        if start_id not in self._entities or end_id not in self._entities:
            return None

        queue: List[Tuple[str, List[str]]] = [(start_id, [start_id])]
        visited: Set[str] = {start_id}

        while queue:
            curr_id, path = queue.pop(0)
            if curr_id == end_id:
                return path

            if len(path) > max_depth:
                continue

            for rel_id in self._adjacency.get(curr_id, []):
                rel = self._relations[rel_id]
                next_id = rel.target_id
                if next_id not in visited:
                    visited.add(next_id)
                    queue.append((next_id, path + [next_id]))

        return None
