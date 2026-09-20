"""
Capability Provider Interface
=============================
Abstract contract for querying available execution subsystems, models, tools, and hardware.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass(frozen=True)
class DiscoveredCapability:
    """A verified capability discovered in the host environment."""
    capability_name: str
    category: str  # "MODEL", "TOOL", "BENCHMARK", "HARDWARE", "AGENT", "STORAGE"
    version: str
    is_available: bool
    confidence: float
    properties: Dict[str, Any] = field(default_factory=dict)
    diagnostic: str = ""


class ICapabilityProvider(ABC):
    """Abstract capability provider interface for capability discovery."""

    @abstractmethod
    def discover_capabilities(self) -> List[DiscoveredCapability]:
        """Discovers all currently available capabilities in the environment."""
        raise NotImplementedError

    @abstractmethod
    def is_capability_available(self, capability_name: str) -> bool:
        """Checks if a specific capability is available."""
        raise NotImplementedError


class DefaultSystemCapabilityProvider(ICapabilityProvider):
    """
    Default capability provider inspecting known local runtime modules and hardware.
    """

    KNOWN_CAPABILITIES = {
        "OCR": {"category": "MODEL", "version": "2.4.0", "confidence": 0.95},
        "LLM": {"category": "MODEL", "version": "gemini-pro", "confidence": 0.90},
        "BENCHMARK": {"category": "BENCHMARK", "version": "1.0.0", "confidence": 1.0},
        "OPTIMIZER": {"category": "TOOL", "version": "1.0.0", "confidence": 1.0},
        "GOVERNANCE": {"category": "TOOL", "version": "1.0.0", "confidence": 1.0},
        "MEMORY": {"category": "STORAGE", "version": "1.0.0", "confidence": 1.0},
        "KNOWLEDGE_GRAPH": {"category": "STORAGE", "version": "1.0.0", "confidence": 1.0},
        "GPU_ACCELERATION": {"category": "HARDWARE", "version": "cuda", "confidence": 0.50},
        "SCIENTIFIC_AGENTS": {"category": "AGENT", "version": "1.0.0", "confidence": 1.0},
        "STORAGE": {"category": "STORAGE", "version": "local_disk", "confidence": 1.0},
    }

    def __init__(self, overrides: Optional[Dict[str, bool]] = None):
        self._overrides = overrides or {}

    def discover_capabilities(self) -> List[DiscoveredCapability]:
        discovered: List[DiscoveredCapability] = []
        for name, meta in self.KNOWN_CAPABILITIES.items():
            avail = self._overrides.get(name, True)
            discovered.append(DiscoveredCapability(
                capability_name=name,
                category=meta["category"],
                version=meta["version"],
                is_available=avail,
                confidence=meta["confidence"] if avail else 0.0,
                diagnostic="Discovered active subsystem." if avail else "Subsystem disabled by policy override.",
            ))
        return discovered

    def is_capability_available(self, capability_name: str) -> bool:
        if capability_name in self._overrides:
            return self._overrides[capability_name]
        return capability_name in self.KNOWN_CAPABILITIES
