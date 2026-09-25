"""
Enterprise Bounded Contexts Package.
Contains all 12 independent verification bounded contexts.
"""
from .runtime import BoundedContextsRuntime, get_contexts_runtime

__all__ = ["BoundedContextsRuntime", "get_contexts_runtime"]
