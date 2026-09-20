"""Data Lineage Graph Edges (Phase 8B)."""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class LineageEdgeType(str, enum.Enum):
    """Directed dependency relationships in data lineage graphs."""
    CREATED = "CREATED"
    READ = "READ"
    WRITTEN = "WRITTEN"
    TRANSFORMED = "TRANSFORMED"
    DERIVED_FROM = "DERIVED_FROM"
    USED_BY = "USED_BY"
    GENERATED_BY = "GENERATED_BY"
    APPROVED_BY = "APPROVED_BY"


class LineageEdge(BaseModel):
    """Directed edge representing data flow or transformation dependency."""
    edge_id: str
    source_node_id: str
    target_node_id: str
    edge_type: LineageEdgeType
    organization_id: str
    actor_id: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
