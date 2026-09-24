"""
Capability Requirement Model
============================
Defines required subsystems, models, tools, and hardware needed for goal execution.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict


class CapabilityCriticality(str, Enum):
    MANDATORY = "MANDATORY"
    RECOMMENDED = "RECOMMENDED"
    OPTIONAL = "OPTIONAL"


@dataclass(frozen=True)
class CapabilityRequirement:
    """A specific capability requirement for an autonomous goal."""
    capability_name: str
    category: str  # "MODEL", "TOOL", "BENCHMARK", "HARDWARE", "AGENT", "STORAGE"
    criticality: CapabilityCriticality = CapabilityCriticality.MANDATORY
    min_version: str = "1.0.0"
    min_confidence: float = 0.80
    properties: Dict[str, Any] = field(default_factory=dict)
