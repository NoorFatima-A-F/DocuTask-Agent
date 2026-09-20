"""
Enterprise Decision Subsystem Exception Hierarchy.
Provides domain exceptions for decision evaluation, policy violations, governance conflicts, and risk thresholds.
"""

from app.agents.exceptions import AgentException


class DecisionException(AgentException):
    """Base exception for all decision engine errors."""
    pass


class PolicyViolationException(DecisionException):
    """Raised when an operation violates a mandatory enterprise policy."""
    pass


class GovernanceException(DecisionException):
    """Raised when governance or approval requirements are not satisfied."""
    pass


class RiskThresholdExceededException(DecisionException):
    """Raised when estimated risk score exceeds maximum allowed threshold."""
    pass


class DecisionEvaluationException(DecisionException):
    """Raised when decision evaluation fails due to conflicting rules or missing evaluation parameters."""
    pass
