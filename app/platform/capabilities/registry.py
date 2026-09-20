"""
Platform Capability Registry.
Allows modules and plugins to advertise capabilities and enables dynamic discovery.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from ..kernel.versioning import SemanticVersion


@dataclass
class CapabilityDescriptor:
    """Descriptor of an advertised platform capability."""
    name: str  # e.g., 'document.ocr', 'ai.embedding', 'tool_calling'
    provider: str  # Module or plugin name
    version: SemanticVersion = field(default_factory=lambda: SemanticVersion(1, 0, 0))
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "provider": self.provider,
            "version": str(self.version),
            "metadata": self.metadata,
            "registered_at": self.registered_at.isoformat(),
        }


class CapabilityRegistry:
    """Central registry of all advertised system capabilities."""

    def __init__(self):
        self._capabilities: Dict[str, CapabilityDescriptor] = {}

    def register_capability(
        self,
        name: str,
        provider: str,
        version: Optional[SemanticVersion] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CapabilityDescriptor:
        """Advertise a new capability from a provider."""
        descriptor = CapabilityDescriptor(
            name=name,
            provider=provider,
            version=version or SemanticVersion(1, 0, 0),
            metadata=metadata or {},
        )
        self._capabilities[name] = descriptor
        return descriptor

    def unregister_capability(self, name: str) -> None:
        """Remove a capability from the registry."""
        self._capabilities.pop(name, None)

    def has_capability(self, name: str) -> bool:
        """Check if a capability is currently available."""
        return name in self._capabilities

    def get_provider(self, name: str) -> Optional[str]:
        """Get the provider module/plugin name for a capability."""
        cap = self._capabilities.get(name)
        return cap.provider if cap else None

    def get_capability(self, name: str) -> Optional[CapabilityDescriptor]:
        """Get capability descriptor by name."""
        return self._capabilities.get(name)

    def list_capabilities(self, provider: Optional[str] = None) -> List[CapabilityDescriptor]:
        """List all capabilities, optionally filtered by provider."""
        if provider is None:
            return list(self._capabilities.values())
        return [c for c in self._capabilities.values() if c.provider == provider]
