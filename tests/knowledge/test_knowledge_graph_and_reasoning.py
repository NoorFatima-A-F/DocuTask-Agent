"""
Tests for KnowledgeGraphEngine.
"""

import pytest
from app.knowledge.graph.engine import KnowledgeGraphEngine


def test_knowledge_graph_entities_and_traversals():
    graph = KnowledgeGraphEngine()

    # Add Entities
    e_alice = graph.add_entity("ent-user-1", "Person", "Alice Smith", {"role": "CISO"})
    e_policy = graph.add_entity("ent-doc-1", "Policy", "Access Control Policy", {"version": "2.0"})
    e_dept = graph.add_entity("ent-dept-1", "Department", "Information Security", {})
    e_acme = graph.add_entity("ent-org-1", "Company", "Acme Corporation", {})

    # Add Relationships
    graph.add_relation("ent-user-1", "ent-doc-1", "approved_by")
    graph.add_relation("ent-user-1", "ent-dept-1", "belongs_to")
    graph.add_relation("ent-dept-1", "ent-org-1", "belongs_to")
    graph.add_relation("ent-doc-1", "ent-org-1", "applies_to")

    # Verify entity retrieval
    assert graph.get_entity("ent-user-1").name == "Alice Smith"

    # Outgoing neighbors of Alice
    neighbors = graph.get_neighbors("ent-user-1", direction="outgoing")
    assert len(neighbors) == 2
    rel_types = [r.relation_type for r, target in neighbors]
    assert "approved_by" in rel_types
    assert "belongs_to" in rel_types

    # Specific relation filter
    dept_neighbor = graph.get_neighbors("ent-user-1", relation_type="belongs_to")
    assert len(dept_neighbor) == 1
    assert dept_neighbor[0][1].name == "Information Security"

    # Multi-hop shortest path: Alice -> Acme Corporation
    path = graph.find_path("ent-user-1", "ent-org-1", max_depth=3)
    assert path is not None
    assert path[0] == "ent-user-1"
    assert path[-1] == "ent-org-1"
    assert len(path) == 3  # Alice -> InfoSec -> Acme
