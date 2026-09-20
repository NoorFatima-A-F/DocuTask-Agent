"""
Tool Validation Guards.
Provides fail-fast validation for tool descriptors, configurations, and IDs.
"""

from app.agents.tools.descriptor import ToolDescriptor
from app.agents.tools.exceptions import ToolValidationException


class ToolValidator:
    """Validator guards for tool descriptors and configurations."""

    @staticmethod
    def validate_descriptor(descriptor: ToolDescriptor) -> None:
        """Validates tool descriptor fields and raises ToolValidationException on failure."""
        if not descriptor.identity.tool_id or not descriptor.identity.tool_id.strip():
            raise ToolValidationException("Tool ID cannot be empty.")
        if not descriptor.identity.name or not descriptor.identity.name.strip():
            raise ToolValidationException("Tool name cannot be empty.")
        if not descriptor.metadata.supported_capabilities:
            raise ToolValidationException("Tool must support at least one capability.")
