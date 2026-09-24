"""
Scientific Knowledge Node Models (Phase 83C)
===========================================
Strongly typed entities in the scientific knowledge graph.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from research_validation.knowledge_graph.ontology import EntityType
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class KnowledgeNode:
    """Base immutable node in the scientific knowledge graph."""
    node_id: str
    entity_type: EntityType
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    node_digest_sha256: str = field(default="")

    def compute_digest(self) -> str:
        payload = {
            "node_id": self.node_id,
            "entity_type": self.entity_type.value,
            "name": self.name,
            "properties": self.properties,
        }
        return hash_canonical_json(payload)


@dataclass(frozen=True)
class ExperimentNode(KnowledgeNode):
    """Represents a specific executed or planned scientific experiment."""
    pass


@dataclass(frozen=True)
class DatasetNode(KnowledgeNode):
    """Represents a benchmark or training dataset."""
    pass


@dataclass(frozen=True)
class MetricNode(KnowledgeNode):
    """Represents an observed or derived quantitative metric."""
    pass


@dataclass(frozen=True)
class ModelNode(KnowledgeNode):
    """Represents a machine learning or rule-based document model."""
    pass


@dataclass(frozen=True)
class EnvironmentNode(KnowledgeNode):
    """Represents the computational runtime and hardware environment."""
    pass


@dataclass(frozen=True)
class HypothesisNode(KnowledgeNode):
    """Represents an active or tested scientific hypothesis."""
    pass


@dataclass(frozen=True)
class ClaimNode(KnowledgeNode):
    """Represents an empirical or scientific claim."""
    pass


def create_node(
    node_id: str,
    entity_type: EntityType,
    name: str,
    properties: Optional[Dict[str, Any]] = None,
) -> KnowledgeNode:
    """Factory helper to construct a strongly-typed, hash-sealed KnowledgeNode."""
    props = properties or {}
    payload = {
        "node_id": node_id,
        "entity_type": entity_type.value,
        "name": name,
        "properties": props,
    }
    digest = hash_canonical_json(payload)
    
    node_cls_map = {
        EntityType.EXPERIMENT: ExperimentNode,
        EntityType.DATASET: DatasetNode,
        EntityType.METRIC: MetricNode,
        EntityType.MODEL: ModelNode,
        EntityType.ENVIRONMENT: EnvironmentNode,
        EntityType.HYPOTHESIS: HypothesisNode,
        EntityType.CLAIM: ClaimNode,
    }
    cls = node_cls_map.get(entity_type, KnowledgeNode)
    return cls(
        node_id=node_id,
        entity_type=entity_type,
        name=name,
        properties=props,
        node_digest_sha256=digest,
    )
