"""
Enterprise Planning Exception Hierarchy.
Provides domain exceptions for plan validation, DAG cycles, missing dependencies,
unreachable nodes, broken references, and simulation errors.
"""

from app.agents.exceptions import AgentException


class PlanningException(AgentException):
    """Base exception for all planning subsystem errors."""
    pass


class CyclicDependencyException(PlanningException):
    """Raised when a circular dependency or loop cycle is detected in the plan graph."""
    pass


class InvalidPlanException(PlanningException):
    """Raised when a plan violates structural, constraint, or timeline requirements."""
    pass


class UnreachableNodeException(PlanningException):
    """Raised when a node in the planning graph cannot be reached from entry nodes."""
    pass


class MissingDependencyException(PlanningException):
    """Raised when a task node depends on an unresolvable or non-existent prerequisite."""
    pass


class DuplicateNodeException(PlanningException):
    """Raised when duplicate node IDs are detected within the same planning graph."""
    pass


class PlanValidationException(PlanningException):
    """Raised when plan validation rules fail."""
    pass
