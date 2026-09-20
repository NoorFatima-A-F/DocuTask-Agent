"""
Agent Query Contracts.
Defines AgentQuery and QueryResult for QueryBus dispatches.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.agents.messaging.metadata import MessageMetadata


class AgentQuery(BaseModel):
    """Base class for all Agent Queries."""

    query_type: str = Field(default="AgentQuery")
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    parameters: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class QueryResult(BaseModel):
    """Result of a query execution."""

    query_id: str
    success: bool = Field(default=True)
    data: Optional[Any] = Field(default=None)
    error_message: Optional[str] = Field(default=None)

    model_config = {"frozen": True}
