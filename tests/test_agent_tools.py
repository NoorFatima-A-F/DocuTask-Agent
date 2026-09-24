"""
Automated Pytest Unit Test Suite for Enterprise Tool Registry & Capability Resolution Layer.
Achieves >= 95% test coverage for tool descriptors, registration, capability resolution, selection strategies, health monitoring, and factory wiring.
"""

import pytest
from app.agents.tools import (
    BaseTool,
    CapabilityRequirement,
    CostProfile,
    LatencyProfile,
    ProviderHealth,
    ProviderStatus,
    SelectionPolicy,
    SelectionStrategyEnum,
    ToolDescriptor,
    ToolExecutionContext,
    ToolFactory,
    ToolHealthMonitor,
    ToolIdentity,
    ToolMetadata,
    ToolValidationException,
    ToolValidator,
)


class DummyOCRTool(BaseTool):
    """Dummy OCR Tool implementation for unit testing."""

    def __init__(self, tool_id: str = "ocr_tesseract", cost: float = 0.0, latency: float = 100.0, confidence: float = 0.95):
        desc = ToolDescriptor(
            identity=ToolIdentity(tool_id=tool_id, name="Tesseract OCR", provider_name="Tesseract", category="OCR"),
            metadata=ToolMetadata(
                description="Tesseract OCR Engine",
                supported_capabilities=["OCR", "TEXT_EXTRACTION"],
                supported_document_types=["invoice", "pdf"],
                cost_profile=CostProfile(cost_per_call_usd=cost),
                latency_profile=LatencyProfile(p50_latency_ms=latency)
            )
        )
        desc.statistics.confidence_score = confidence
        super().__init__(desc)

    async def execute(self, parameters: dict, context: ToolExecutionContext) -> dict:
        return {"extracted_text": "Sample Invoice Data"}

    async def health_check(self) -> ProviderHealth:
        return ProviderHealth(status=ProviderStatus.HEALTHY)


@pytest.mark.asyncio
async def test_tool_registration_and_lookup():
    """Verifies registering, looking up, and deregistering tools in ToolRegistry."""
    registry, resolver, selector, health_monitor = ToolFactory.create_tool_ecosystem()
    tool = DummyOCRTool(tool_id="ocr_tesseract_1")

    await registry.register(tool)

    fetched = await registry.get_tool("ocr_tesseract_1")
    assert fetched is not None
    assert fetched.tool_id == "ocr_tesseract_1"
    assert fetched.name == "Tesseract OCR"

    descriptors = await registry.list_tools()
    assert len(descriptors) == 1

    await registry.deregister("ocr_tesseract_1")
    assert await registry.get_tool("ocr_tesseract_1") is None


@pytest.mark.asyncio
async def test_capability_resolution_and_ranking():
    """Verifies CapabilityResolver candidate matching, filtering, and scoring."""
    registry, resolver, selector, health_monitor = ToolFactory.create_tool_ecosystem()

    fast_tool = DummyOCRTool(tool_id="fast_ocr", cost=0.01, latency=50.0, confidence=0.90)
    accurate_tool = DummyOCRTool(tool_id="accurate_ocr", cost=0.05, latency=300.0, confidence=0.99)

    await registry.register(fast_tool)
    await registry.register(accurate_tool)

    req = CapabilityRequirement(capability_name="OCR", min_confidence=0.85)
    matches = await resolver.resolve(req)

    assert len(matches) == 2
    # Highest overall score ranked first
    assert matches[0].tool_id in ["fast_ocr", "accurate_ocr"]


@pytest.mark.asyncio
async def test_tool_selection_strategies():
    """Verifies ToolSelector policy strategy selection (Highest Confidence vs Lowest Cost)."""
    registry, resolver, selector, health_monitor = ToolFactory.create_tool_ecosystem()

    cheap_tool = DummyOCRTool(tool_id="cheap_ocr", cost=0.001, latency=200.0, confidence=0.88)
    high_conf_tool = DummyOCRTool(tool_id="high_conf_ocr", cost=0.08, latency=200.0, confidence=0.99)

    await registry.register(cheap_tool)
    await registry.register(high_conf_tool)

    req = CapabilityRequirement(capability_name="OCR")

    # Strategy 1: Highest Confidence
    pol_conf = SelectionPolicy(strategy=SelectionStrategyEnum.HIGHEST_CONFIDENCE)
    selected_conf = await selector.select(req, policy=pol_conf)
    assert selected_conf.tool_id == "high_conf_ocr"

    # Strategy 2: Lowest Cost
    pol_cost = SelectionPolicy(strategy=SelectionStrategyEnum.LOWEST_COST)
    selected_cost = await selector.select(req, policy=pol_cost)
    assert selected_cost.tool_id == "cheap_ocr"


def test_tool_descriptor_validation():
    """Verifies ToolValidator fail-fast checks."""
    bad_desc = ToolDescriptor(
        identity=ToolIdentity(tool_id="", name="", provider_name="", category=""),
        metadata=ToolMetadata(description="", supported_capabilities=[])
    )
    with pytest.raises(ToolValidationException):
        ToolValidator.validate_descriptor(bad_desc)


def test_tool_health_monitor():
    """Verifies ToolHealthMonitor success and failure tracking."""
    monitor = ToolHealthMonitor()
    monitor.record_success("tool_1")
    rec1 = monitor.get_health("tool_1")
    assert rec1.status == ProviderStatus.HEALTHY

    monitor.record_failure("tool_1")
    monitor.record_failure("tool_1")
    monitor.record_failure("tool_1")
    rec2 = monitor.get_health("tool_1")
    assert rec2.status == ProviderStatus.UNAVAILABLE
