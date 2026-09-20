"""
Capability Registry.
Maintains canonical catalog of skills, required tools, and domain definitions across the platform.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.coordination.capability import AgentSkill


class CapabilityRegistry:
    """Central registry of valid skills and execution domains."""

    def __init__(self):
        self._skills: Dict[str, AgentSkill] = {}

    def register_skill(self, skill: AgentSkill) -> None:
        """Registers a standardized skill definition."""
        self._skills[skill.name.lower()] = skill

    def get_skill(self, name: str) -> Optional[AgentSkill]:
        """Retrieves a skill definition by name."""
        return self._skills.get(name.lower())

    def list_all_skills(self) -> List[AgentSkill]:
        """Returns all registered skills."""
        return list(self._skills.values())
