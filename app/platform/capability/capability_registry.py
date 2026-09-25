"""Dynamic Capability Registry and Pareto Resolver.

Allows plugins to advertise implementations for abstract capabilities (OCR, Table Extraction,
HIPAA Validation) and enables the planner to resolve optimal providers on demand.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.platform.capability.capability_model import (
    CapabilityDefinition,
    CapabilityProvider,
)


class CapabilityRegistry:
    def __init__(self):
        self._capabilities: Dict[str, CapabilityDefinition] = {}

    def register_capability(
        self,
        capability_name: str,
        category: str,
        description: str,
        input_schema: Optional[Dict[str, Any]] = None,
        output_schema: Optional[Dict[str, Any]] = None,
    ) -> CapabilityDefinition:
        if capability_name not in self._capabilities:
            self._capabilities[capability_name] = CapabilityDefinition(
                capability_name=capability_name,
                category=category,
                description=description,
                input_schema=input_schema or {},
                output_schema=output_schema or {},
            )
        return self._capabilities[capability_name]

    def register_provider(
        self,
        capability_name: str,
        provider: CapabilityProvider,
    ) -> None:
        if capability_name not in self._capabilities:
            self.register_capability(
                capability_name=capability_name,
                category="general",
                description=f"Auto-registered capability {capability_name}",
            )
        self._capabilities[capability_name].providers[provider.provider_id] = provider

    def unregister_provider(self, capability_name: str, provider_id: str) -> bool:
        if capability_name in self._capabilities:
            if provider_id in self._capabilities[capability_name].providers:
                del self._capabilities[capability_name].providers[provider_id]
                return True
        return False

    def get_capability(self, capability_name: str) -> Optional[CapabilityDefinition]:
        return self._capabilities.get(capability_name)

    def list_capabilities(self) -> List[CapabilityDefinition]:
        return list(self._capabilities.values())

    def clear(self) -> None:
        self._capabilities.clear()


class CapabilityResolver:
    @staticmethod
    def resolve_provider(
        registry: CapabilityRegistry,
        capability_name: str,
        max_latency_ms: Optional[float] = None,
        max_cost_usd: Optional[float] = None,
        min_quality: Optional[float] = None,
    ) -> Optional[CapabilityProvider]:
        cap = registry.get_capability(capability_name)
        if not cap or not cap.providers:
            return None

        candidates = [p for p in cap.providers.values() if p.health_status == "HEALTHY"]
        if not candidates:
            return None

        # Filter by constraints if supplied
        if max_latency_ms is not None:
            candidates = [p for p in candidates if p.p95_latency_ms <= max_latency_ms] or candidates
        if max_cost_usd is not None:
            candidates = [p for p in candidates if p.cost_per_unit_usd <= max_cost_usd] or candidates
        if min_quality is not None:
            candidates = [p for p in candidates if p.quality_score >= min_quality] or candidates

        # Score candidates: utility = (quality * 0.5) - (cost * 0.25) - (latency * 0.25)
        def score(p: CapabilityProvider) -> float:
            return (p.quality_score * 0.5) - (p.cost_per_unit_usd / 0.05 * 0.25) - (p.p95_latency_ms / 1000.0 * 0.25)

        candidates.sort(key=score, reverse=True)
        return candidates[0]


global_capability_registry = CapabilityRegistry()
