"""
Decision Evaluation Strategies.
"""

from enum import Enum


class DecisionStrategy(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    WEIGHTED = "WEIGHTED"
    RISK_ADJUSTED = "RISK_ADJUSTED"
