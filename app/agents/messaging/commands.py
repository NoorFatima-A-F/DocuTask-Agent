"""
Agent Command Contracts.
Defines AgentCommand and CommandResult models for CommandBus dispatches.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.agents.messaging.metadata import MessageMetadata


class AgentCommand(BaseModel):
    """Base class for all Agent Commands."""

    command_type: str = Field(default="AgentCommand")
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    parameters: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class CommandResult(BaseModel):
    """Result of a command execution."""

    command_id: str
    success: bool = Field(default=True)
    result_data: Optional[Any] = Field(default=None)
    error_message: Optional[str] = Field(default=None)

    model_config = {"frozen": True}
