"""
Capability Graph.
Represents hierarchical and dependency relationships between skills and tasks as a DAG.
"""

from typing import Dict, List, Set
from pydantic import BaseModel, Field


class CapabilityGraph(BaseModel):
    """Directed acyclic graph tracking prerequisites and composability between capabilities."""
    nodes: Set[str] = Field(default_factory=set)
    prerequisites: Dict[str, List[str]] = Field(default_factory=dict)

    def add_capability(self, name: str, prerequisites: List[str] = None) -> None:
        """Adds a capability and its required prerequisite capabilities."""
        norm_name = name.lower()
        self.nodes.add(norm_name)
        if prerequisites:
            self.prerequisites[norm_name] = [p.lower() for p in prerequisites]
            for p in prerequisites:
                self.nodes.add(p.lower())

    def get_prerequisites(self, name: str) -> List[str]:
        """Returns all direct prerequisites for a capability."""
        return self.prerequisites.get(name.lower(), [])
