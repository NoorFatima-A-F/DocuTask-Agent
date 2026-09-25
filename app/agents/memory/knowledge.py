"""
Knowledge Graph Domain Models.
Defines KnowledgeItem, KnowledgeGraphNode, KnowledgeEdge, KnowledgeCluster, KnowledgeSource, and KnowledgeCitation.
Supports Facts, Rules, Patterns, Examples, Templates, Schemas, and Historical observations.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class KnowledgeSource(BaseModel):
    """Origin of a knowledge item."""
    source_type: str = Field(default="EXECUTION_OBSERVATION")
    uri: Optional[str] = Field(default=None)
    model_config = {"frozen": True}


class KnowledgeItem(BaseModel):
    """Knowledge item representation."""
    item_id: UUID = Field(default_factory=uuid4)
    category: str = Field(default="FACT")  # FACT, RULE, PATTERN, EXAMPLE, TEMPLATE, SCHEMA
    topic: str
    content: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    source: KnowledgeSource = Field(default_factory=KnowledgeSource)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = {"frozen": True}


class KnowledgeGraphNode(BaseModel):
    """Node in a knowledge graph."""
    node_id: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class KnowledgeEdge(BaseModel):
    """Edge connecting two nodes in a knowledge graph."""
    edge_id: str
    source_node_id: str
    target_node_id: str
    relation_type: str = Field(default="RELATED_TO")
    weight: float = Field(default=1.0, ge=0.0)
    model_config = {"frozen": True}


class KnowledgeCluster(BaseModel):
    """Cluster of related knowledge graph nodes and items."""
    cluster_id: str
    name: str
    nodes: List[KnowledgeGraphNode] = Field(default_factory=list)
    edges: List[KnowledgeEdge] = Field(default_factory=list)
    model_config = {"frozen": True}
