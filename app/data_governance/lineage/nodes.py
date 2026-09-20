"""Data Lineage Graph Nodes (Phase 8B)."""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class LineageNodeType(str, enum.Enum):
    """Supported entity types in a data lineage graph."""
    DATASET = "DATASET"
    DOCUMENT = "DOCUMENT"
    WORKFLOW = "WORKFLOW"
    TASK = "TASK"
    AGENT = "AGENT"
    CONNECTOR = "CONNECTOR"
    MODEL = "MODEL"
    PROMPT = "PROMPT"
    USER = "USER"
    SYSTEM = "SYSTEM"


class LineageNode(BaseModel):
    """Node in the enterprise data lineage DAG."""
    node_id: str
    node_type: LineageNodeType
    label: str
    organization_id: str
    workspace_id: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
