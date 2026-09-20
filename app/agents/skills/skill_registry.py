"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Skill Registry.
Manages cognitive agent skills (Extraction, Classification, Summarization,
Translation, Search, Validation, Planning, Analysis, Compliance, OCR, Scheduling).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentSkill:
    """A discrete cognitive or operational skill exposed to autonomous agents."""
    name: str
    version: str = "1.0.0"
    capability: str = "general"
    cost_per_call_usd: float = 0.001
    required_permissions: List[str] = field(default_factory=list)
    description: str = ""
    handler: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "capability": self.capability,
            "cost_per_call_usd": self.cost_per_call_usd,
            "required_permissions": self.required_permissions,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }


class SkillRegistry:
    """
    Central catalog of registered cognitive skills available to worker
    and supervisor agents.
    """

    DEFAULT_SKILLS = [
        ("extraction", "document.extraction", 0.005, ["data:read"], "Extract structured data from unstructured text/documents"),
        ("classification", "document.classification", 0.002, ["data:read"], "Categorize documents or text into tax/legal/financial classes"),
        ("summarization", "text.summarization", 0.003, ["data:read"], "Generate concise summaries of documents and reasoning traces"),
        ("translation", "language.translation", 0.002, ["data:read"], "Translate multi-lingual content"),
        ("search", "knowledge.search", 0.001, ["data:read"], "Retrieve relevant context from organizational knowledge"),
        ("validation", "data.validation", 0.001, ["data:read"], "Validate schemas, mathematical constraints, and data integrity"),
        ("planning", "agent.planning", 0.005, ["agent:plan"], "Decompose complex business goals into dependency graphs"),
        ("analysis", "document.analysis", 0.004, ["data:read"], "Deep cognitive analysis of clauses, risks, and terms"),
        ("compliance", "governance.compliance", 0.003, ["governance:read"], "Verify regulatory, policy, and tax compliance rules"),
        ("ocr", "document.ocr", 0.010, ["data:read"], "Optical character recognition and layout analysis"),
        ("scheduling", "platform.scheduling", 0.001, ["schedule:write"], "Schedule delayed tasks and deadline timers"),
    ]

    def __init__(self, load_defaults: bool = True):
        self._skills: Dict[str, AgentSkill] = {}
        if load_defaults:
            for name, cap, cost, perms, desc in self.DEFAULT_SKILLS:
                self.register(AgentSkill(
                    name=name,
                    capability=cap,
                    cost_per_call_usd=cost,
                    required_permissions=perms,
                    description=desc,
                ))

    def register(self, skill: AgentSkill) -> AgentSkill:
        """Registers a cognitive skill in the platform registry."""
        self._skills[skill.name] = skill
        logger.info(f"Registered Skill '{skill.name}' v{skill.version} [Capability: {skill.capability}]")
        return skill

    def get(self, name: str) -> Optional[AgentSkill]:
        """Retrieves a skill by name."""
        return self._skills.get(name)

    def find_by_capability(self, capability: str) -> List[AgentSkill]:
        """Finds all skills supporting a given capability identifier."""
        return [s for s in self._skills.values() if s.capability.lower() == capability.lower()]

    def list_all(self) -> List[AgentSkill]:
        """Returns all registered skills."""
        return list(self._skills.values())
