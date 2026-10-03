"""
Autonomous Goal Intelligence Exceptions
=======================================
Strongly typed domain and validation exceptions for the goal and mission management system.
"""

from typing import Any, Dict, List, Optional


class GoalIntelligenceError(Exception):
    """Base exception for all goal intelligence errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class GoalValidationError(GoalIntelligenceError):
    """Raised when a goal fails validation rules."""
    def __init__(self, message: str, validation_errors: Optional[List[str]] = None):
        super().__init__(message, details={"validation_errors": validation_errors or []})
        self.validation_errors = validation_errors or []


class InvalidStateTransitionError(GoalIntelligenceError):
    """Raised when an illegal FSM state transition is attempted."""
    def __init__(self, current_state: str, attempted_state: str, rationale: str = ""):
        msg = f"Cannot transition mission from '{current_state}' to '{attempted_state}'. {rationale}".strip()
        super().__init__(msg, details={"current_state": current_state, "attempted_state": attempted_state})
        self.current_state = current_state
        self.attempted_state = attempted_state


class MissingCapabilityError(GoalIntelligenceError):
    """Raised when a mandatory capability is unavailable in the environment."""
    def __init__(self, missing_capabilities: List[str]):
        msg = f"Missing mandatory capabilities: {', '.join(missing_capabilities)}"
        super().__init__(msg, details={"missing_capabilities": missing_capabilities})
        self.missing_capabilities = missing_capabilities


class CircularDependencyError(GoalIntelligenceError):
    """Raised when dependency analysis discovers a cycle in goals or tasks."""
    def __init__(self, cycle_path: List[str]):
        msg = f"Circular dependency detected in graph: {' -> '.join(cycle_path)}"
        super().__init__(msg, details={"cycle_path": cycle_path})
        self.cycle_path = cycle_path


class BudgetExceededError(GoalIntelligenceError):
    """Raised when estimated budget exceeds maximum permissible constraints."""
    def __init__(self, resource_type: str, requested: float, limit: float):
        msg = f"Budget exceeded for {resource_type}: requested {requested:.2f}, limit {limit:.2f}"
        super().__init__(msg, details={"resource_type": resource_type, "requested": requested, "limit": limit})


class RiskThresholdExceededError(GoalIntelligenceError):
    """Raised when evaluated risk exceeds acceptable tolerance without approved mitigation."""
    def __init__(self, risk_score: float, max_acceptable: float, blocking_risks: List[str]):
        msg = f"Risk score {risk_score:.2f} exceeds threshold {max_acceptable:.2f}"
        super().__init__(msg, details={"risk_score": risk_score, "max_acceptable": max_acceptable, "blocking_risks": blocking_risks})


class EntityNotFoundError(GoalIntelligenceError):
    """Raised when a requested goal or mission entity does not exist."""
    def __init__(self, entity_type: str, entity_id: str):
        msg = f"{entity_type} with ID '{entity_id}' was not found."
        super().__init__(msg, details={"entity_type": entity_type, "entity_id": entity_id})
