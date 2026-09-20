"""
Workflow Definition Model.
Immutable, versioned specification of a workflow graph, input schemas, and timeout policies.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.workflow.workflow_graph import WorkflowGraph
from app.agents.workflow.workflow_version import WorkflowVersion


class WorkflowDefinition(BaseModel):
    """Immutable specification defining a reusable workflow DAG and its metadata."""
    definition_id: UUID = Field(default_factory=uuid4)
    name: str
    description: str = ""
    version: WorkflowVersion = Field(default_factory=WorkflowVersion)
    graph: WorkflowGraph
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
