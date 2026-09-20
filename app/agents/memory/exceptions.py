"""
Enterprise Memory Subsystem Exception Hierarchy.
Provides domain exceptions for memory lookup, provider storage, context window overflow, and snapshot corruption.
"""

from app.agents.exceptions import AgentException


class MemoryException(AgentException):
    """Base exception for all memory subsystem errors."""
    pass


class MemoryNotFoundException(MemoryException):
    """Raised when a requested memory item is not found."""
    pass


class ProviderUnavailableException(MemoryException):
    """Raised when a memory storage provider is offline or unreachable."""
    pass


class ContextWindowExceededException(MemoryException):
    """Raised when context assembly exceeds token budget limits."""
    pass


class SnapshotCorruptedException(MemoryException):
    """Raised when a memory snapshot fails verification or checksum validation."""
    pass


class MemoryValidationException(MemoryException):
    """Raised when a memory item fails schema or domain validation."""
    pass
