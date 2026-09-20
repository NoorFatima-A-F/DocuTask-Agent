"""
Goal and Mission Dependency Model
=================================
Defines directed dependencies across goals, tasks, datasets, tools, and knowledge.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class DependencyType(str, Enum):
    GOAL = "GOAL"
    DATA = "DATA"
    EXECUTION = "EXECUTION"
    RESEARCH = "RESEARCH"
    TOOL = "TOOL"
    GOVERNANCE = "GOVERNANCE"
    MEMORY = "MEMORY"
    KNOWLEDGE = "KNOWLEDGE"


@dataclass(frozen=True)
class GoalDependency:
    """A directed dependency required before a goal or mission step can commence."""
    source_id: str
    target_id: str
    dependency_type: DependencyType
    is_blocking: bool = True
    description: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
