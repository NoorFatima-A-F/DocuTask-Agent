"""
Planning Strategy Enumeration.
Defines available planning and decomposition algorithms.
"""

from enum import Enum


class PlanningStrategy(str, Enum):
    TOP_DOWN = "TOP_DOWN"
    BOTTOM_UP = "BOTTOM_UP"
    HIERARCHICAL = "HIERARCHICAL"
    BACKWARD_CHAINING = "BACKWARD_CHAINING"
    FORWARD_CHAINING = "FORWARD_CHAINING"
    LEAST_COST = "LEAST_COST"
    CONSTRAINT_BASED = "CONSTRAINT_BASED"
    GOAL_ORIENTED = "GOAL_ORIENTED"
    REACTIVE = "REACTIVE"
    HYBRID = "HYBRID"
    LLM_GUIDED = "LLM_GUIDED"
    RULE_GUIDED = "RULE_GUIDED"
