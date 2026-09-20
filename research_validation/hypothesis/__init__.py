"""
Autonomous Hypothesis Package (Phase 86C)
=========================================
"""

from research_validation.hypothesis.hypothesis_model import ScientificHypothesis
from research_validation.hypothesis.hypothesis_generator import AutonomousHypothesisGenerator
from research_validation.hypothesis.hypothesis_prioritizer import (
    PrioritizedHypothesis, HypothesisPrioritizer
)

__all__ = [
    "ScientificHypothesis",
    "AutonomousHypothesisGenerator",
    "PrioritizedHypothesis",
    "HypothesisPrioritizer",
]
