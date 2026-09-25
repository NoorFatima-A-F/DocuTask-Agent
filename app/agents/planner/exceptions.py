"""
Enterprise Planner Exception Hierarchy.
Provides domain exceptions for goal analysis, decomposition failures, candidate generation,
reflection critiques, plan repair errors, and adapter failures.
"""

from app.agents.exceptions import AgentException


class PlannerException(AgentException):
    """Base exception for all planning reasoning errors."""
    pass


class GoalAnalysisException(PlannerException):
    """Raised when goal parsing, normalization, or feasibility analysis fails."""
    pass


class TaskDecompositionException(PlannerException):
    """Raised when hierarchical recursive task decomposition fails."""
    pass


class CandidateGenerationException(PlannerException):
    """Raised when candidate plan generation fails to produce feasible plans."""
    pass


class PlanReflectionException(PlannerException):
    """Raised when self-critique identifies unrepairable flaws in a plan candidate."""
    pass


class PlanRepairException(PlannerException):
    """Raised when automatic plan repair fails to resolve structural or policy violations."""
    pass


class AdapterIntegrationException(PlannerException):
    """Raised when LLM, Decision, Memory, or Tool adapter interactions fail."""
    pass
