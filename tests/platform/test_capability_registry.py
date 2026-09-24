"""Tests for Capability Registry and Resolver."""

from app.platform.capability.capability_model import CapabilityProvider
from app.platform.capability.capability_registry import (
    CapabilityRegistry,
    CapabilityResolver,
)


def test_capability_registration_and_pareto_resolution():
    registry = CapabilityRegistry()
    registry.register_capability("perception.ocr", "perception", "Optical Character Recognition")

    p1 = CapabilityProvider(
        provider_id="p1_tesseract",
        plugin_id="plugin.invoice",
        implementation_name="Tesseract Local",
        priority=90,
        cost_per_unit_usd=0.0001,
        p95_latency_ms=120.0,
        quality_score=0.98,
    )
    p2 = CapabilityProvider(
        provider_id="p2_cloud",
        plugin_id="plugin.cloud_ocr",
        implementation_name="Cloud Vision",
        priority=100,
        cost_per_unit_usd=0.0025,
        p95_latency_ms=450.0,
        quality_score=0.995,
    )

    registry.register_provider("perception.ocr", p1)
    registry.register_provider("perception.ocr", p2)

    assert len(registry.list_capabilities()) == 1
    cap = registry.get_capability("perception.ocr")
    assert len(cap.providers) == 2

    # Resolve without constraints -> Pareto optimal (p1 due to much lower cost/latency)
    selected = CapabilityResolver.resolve_provider(registry, "perception.ocr")
    assert selected is not None
    assert selected.provider_id == "p1_tesseract"

    # Unregister provider
    assert registry.unregister_provider("perception.ocr", "p1_tesseract") is True
    assert len(registry.get_capability("perception.ocr").providers) == 1
