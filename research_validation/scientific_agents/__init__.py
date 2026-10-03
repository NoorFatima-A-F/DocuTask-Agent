"""
Scientific Agents Package (Phase 94C)
=====================================
"""

from research_validation.scientific_agents.agent_definitions import (
    ScientificAgentRole, ScientificAgentMessage, ScientificAgentState
)
from research_validation.scientific_agents.scientific_agent_runtime import (
    ResearchDeliberationVerdict, ScientificAgentRuntime
)

__all__ = [
    "ScientificAgentRole",
    "ScientificAgentMessage",
    "ScientificAgentState",
    "ResearchDeliberationVerdict",
    "ScientificAgentRuntime",
]
