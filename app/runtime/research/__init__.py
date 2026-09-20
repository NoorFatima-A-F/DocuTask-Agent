"""
Autonomous Research and Strategy Discovery Module.
"""

from app.runtime.research.hypothesis_generator import HypothesisGenerator, ResearchHypothesis
from app.runtime.research.exploration_strategy import ThompsonSamplingBandit, UCB1Bandit
from app.runtime.research.discovery_validator import DiscoveryValidator, DiscoveryValidationReport
from app.runtime.research.research_engine import AutonomousResearchEngine

__all__ = [
    "HypothesisGenerator",
    "ResearchHypothesis",
    "ThompsonSamplingBandit",
    "UCB1Bandit",
    "DiscoveryValidator",
    "DiscoveryValidationReport",
    "AutonomousResearchEngine",
]
