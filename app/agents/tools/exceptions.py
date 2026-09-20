"""
Enterprise Tool Registry Exception Hierarchy.
Provides domain exceptions for tool lookup, capability resolution, provider health, version conflicts, and validation errors.
"""

from app.agents.exceptions import AgentException


class ToolException(AgentException):
    """Base exception for all tool ecosystem errors."""
    pass


class ToolNotFoundException(ToolException):
    """Raised when a requested tool is not found in the tool registry."""
    pass


class CapabilityNotFoundException(ToolException):
    """Raised when no tool satisfies the requested capability specifications."""
    pass


class ProviderUnavailableException(ToolException):
    """Raised when a tool provider is unhealthy or unavailable."""
    pass


class VersionConflictException(ToolException):
    """Raised when a tool version conflict occurs during registration or resolution."""
    pass


class RegistryException(ToolException):
    """Raised when a tool registry operation fails."""
    pass


class SelectionException(ToolException):
    """Raised when tool selection or candidate evaluation fails."""
    pass


class ToolValidationException(ToolException):
    """Raised when a tool descriptor or configuration fails validation."""
    pass
