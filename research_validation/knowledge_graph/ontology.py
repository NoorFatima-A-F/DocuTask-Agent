"""
Scientific Knowledge Graph Ontology (Phase 83C)
==============================================
Defines the formal vocabulary, entity types, and relationship taxonomies
for autonomous scientific reasoning and hypothesis formation.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Set


class EntityType(str, Enum):
    EXPERIMENT = "EXPERIMENT"
    DATASET = "DATASET"
    METRIC = "METRIC"
    MODEL = "MODEL"
    ENVIRONMENT = "ENVIRONMENT"
    HYPOTHESIS = "HYPOTHESIS"
    CLAIM = "CLAIM"
    FAILURE_MODE = "FAILURE_MODE"
    BENCHMARK = "BENCHMARK"


class RelationshipType(str, Enum):
    EVALUATES = "EVALUATES"
    TRAINED_ON = "TRAINED_ON"
    DERIVED_FROM = "DERIVED_FROM"
    CAUSES = "CAUSES"
    CORRELATES_WITH = "CORRELATES_WITH"
    CONTRADICTS = "CONTRADICTS"
    REPLICATES = "REPLICATES"
    INVALIDATES = "INVALIDATES"
    PRODUCES_METRIC = "PRODUCES_METRIC"
    TESTED_IN_ENV = "TESTED_IN_ENV"
    SUPPORTS_CLAIM = "SUPPORTS_CLAIM"
    REFUTES_CLAIM = "REFUTES_CLAIM"


@dataclass(frozen=True)
class RelationshipConstraint:
    """Formal ontological constraint on edge validity."""
    source_type: EntityType
    relationship: RelationshipType
    target_type: EntityType
    is_transitive: bool = False
    is_symmetric: bool = False


class ScientificOntology:
    """Validator and repository of valid scientific semantic triples."""

    VALID_CONSTRAINTS: Set[RelationshipConstraint] = {
        RelationshipConstraint(EntityType.EXPERIMENT, RelationshipType.EVALUATES, EntityType.MODEL),
        RelationshipConstraint(EntityType.EXPERIMENT, RelationshipType.EVALUATES, EntityType.BENCHMARK),
        RelationshipConstraint(EntityType.EXPERIMENT, RelationshipType.EVALUATES, EntityType.DATASET),
        RelationshipConstraint(EntityType.EXPERIMENT, RelationshipType.PRODUCES_METRIC, EntityType.METRIC),
        RelationshipConstraint(EntityType.EXPERIMENT, RelationshipType.TESTED_IN_ENV, EntityType.ENVIRONMENT),
        RelationshipConstraint(EntityType.EXPERIMENT, RelationshipType.REPLICATES, EntityType.EXPERIMENT),
        RelationshipConstraint(EntityType.EXPERIMENT, RelationshipType.CONTRADICTS, EntityType.EXPERIMENT, is_symmetric=True),
        RelationshipConstraint(EntityType.EXPERIMENT, RelationshipType.SUPPORTS_CLAIM, EntityType.CLAIM),
        RelationshipConstraint(EntityType.EXPERIMENT, RelationshipType.REFUTES_CLAIM, EntityType.CLAIM),
        RelationshipConstraint(EntityType.MODEL, RelationshipType.TRAINED_ON, EntityType.DATASET),
        RelationshipConstraint(EntityType.METRIC, RelationshipType.DERIVED_FROM, EntityType.DATASET),
        RelationshipConstraint(EntityType.METRIC, RelationshipType.CORRELATES_WITH, EntityType.METRIC, is_symmetric=True),
        RelationshipConstraint(EntityType.METRIC, RelationshipType.CAUSES, EntityType.METRIC, is_transitive=True),
        RelationshipConstraint(EntityType.HYPOTHESIS, RelationshipType.SUPPORTS_CLAIM, EntityType.CLAIM),
        RelationshipConstraint(EntityType.HYPOTHESIS, RelationshipType.INVALIDATES, EntityType.CLAIM),
    }

    @classmethod
    def is_valid_triple(cls, source_type: EntityType, rel: RelationshipType, target_type: EntityType) -> bool:
        """Check if a semantic triple matches permitted ontological definitions."""
        for c in cls.VALID_CONSTRAINTS:
            if c.source_type == source_type and c.relationship == rel and c.target_type == target_type:
                return True
        return False
