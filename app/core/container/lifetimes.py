"""
Dependency Injection Lifetimes.
"""

from enum import Enum


class Lifetime(str, Enum):
    """Lifecycle scopes for registered dependencies."""
    SINGLETON = "SINGLETON"
    SCOPED = "SCOPED"
    TRANSIENT = "TRANSIENT"
