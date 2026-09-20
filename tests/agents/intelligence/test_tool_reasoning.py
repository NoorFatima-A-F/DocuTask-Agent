"""Tests for Tool Reasoning Engine (Phase 25.0).

Covers:
- Modality enum and ToolDefinition constraints
- ToolReasoningRegistry cataloging and querying
- ToolSelector multimodal reasoning (handwriting, tables, cost, SLA)
- ToolExecutionPolicy (execution, retries, fallback cascading, telemetry)
"""

from __future__ import annotations

import asyncio
import pytest

from app.agents.tools.reasoning import (
    Modality,
    ToolDefinition,
    ToolExecutionPolicy,
    ToolExecutionResult,
    ToolReasoningRegistry,
    ToolSelectionResult,
    ToolSelector,
)


class TestToolDefinitionAndRegistry:
    @pytest.fixture
    def registry(self):
        return ToolReasoningRegistry()

    def test_default_tools_registered(self, registry):
        assert registry.get("tool_tesseract_ocr") is not None
        assert registry.get("tool_gemini_vision") is not None
        assert registry.get("tool_regex_extractor") is not None
        assert registry.get("tool_llm_json_extractor") is not None
        assert registry.get("tool_math_verifier") is not None
        assert registry.get("tool_compliance_evaluator") is not None

    def test_register_custom_tool(self, registry):
        tool = ToolDefinition(
            tool_id="custom_tool",
            name="Custom Name",
            category="CUSTOM",
            supported_modalities=[Modality.PDF, Modality.JSON],
            cost_per_call=0.005,
        )
        registry.register(tool)
        assert registry.get("custom_tool") == tool
        assert tool.supports_modality(Modality.PDF) is True
        assert tool.supports_modality(Modality.IMAGE) is False

    def test_find_by_category(self, registry):
        ocr_tools = registry.find_by_category("OCR")
        assert len(ocr_tools) >= 2
        categories = {t.category for t in ocr_tools}
        assert categories == {"OCR"}

    def test_find_by_modality(self, registry):
        handwriting_tools = registry.find_by_modality(Modality.HANDWRITING)
        assert len(handwriting_tools) >= 1
        assert handwriting_tools[0].tool_id == "tool_gemini_vision"

    def test_list_all(self, registry):
        tools = registry.list_all()
        assert len(tools) >= 6

    def test_get_nonexistent_returns_none(self, registry):
        assert registry.get("nonexistent_tool") is None


class TestToolSelector:
    @pytest.fixture
    def selector(self):
        reg = ToolReasoningRegistry()
        return ToolSelector(reg)

    def test_select_ocr_default_image(self, selector):
        res = selector.select_tool("OCR", document_modality=Modality.IMAGE)
        assert isinstance(res, ToolSelectionResult)
        assert res.selected_tool.tool_id in ("tool_tesseract_ocr", "tool_gemini_vision")

    def test_select_ocr_with_handwriting_prioritizes_gemini(self, selector):
        res = selector.select_tool("OCR", document_modality=Modality.IMAGE, has_handwriting=True)
        assert res.selected_tool.tool_id == "tool_gemini_vision"
        assert "handwriting" in res.reasoning.lower()

    def test_select_ocr_with_complex_tables_prioritizes_vision(self, selector):
        res = selector.select_tool("OCR", document_modality=Modality.IMAGE, has_complex_tables=True)
        assert res.selected_tool.tool_id == "tool_gemini_vision"
        assert "tabular" in res.reasoning.lower()

    def test_select_extraction_cost_sensitive_prioritizes_regex(self, selector):
        res = selector.select_tool("EXTRACTION", cost_sensitive=True)
        assert res.selected_tool.tool_id == "tool_regex_extractor"

    def test_select_extraction_high_accuracy_prioritizes_llm(self, selector):
        res = selector.select_tool("EXTRACTION", min_accuracy=0.98, cost_sensitive=False)
        assert res.selected_tool.tool_id == "tool_llm_json_extractor"

    def test_select_tool_nonexistent_category_raises(self, selector):
        with pytest.raises(KeyError, match="No tools registered for category"):
            selector.select_tool("QUANTUM_COMPUTING")

    def test_fallback_tool_configured_when_alternatives_exist(self, selector):
        res = selector.select_tool("OCR", document_modality=Modality.IMAGE)
        assert res.fallback_tool is not None
        assert res.fallback_tool.tool_id != res.selected_tool.tool_id


@pytest.fixture
def setup_policy():
    reg = ToolReasoningRegistry()
    return reg, ToolExecutionPolicy(reg)


class TestToolExecutionPolicy:
    @pytest.mark.asyncio
    async def test_execute_primary_tool_success(self, setup_policy):
        _, policy = setup_policy
        res = await policy.execute_with_policy("tool_math_verifier", {"subtotal": 10.0, "tax": 1.0})
        assert res.success is True
        assert res.tool_id == "tool_math_verifier"
        assert res.was_fallback is False
        assert res.execution_time_ms >= 0.0

    @pytest.mark.asyncio
    async def test_execute_with_fallback_when_primary_fails(self, setup_policy):
        reg, policy = setup_policy

        # Custom failing primary tool
        async def failing_exec(args):
            raise ConnectionError("Tesseract worker crashed")

        failing_tool = ToolDefinition(
            tool_id="tool_failing_ocr",
            name="Failing OCR",
            category="OCR",
            executor=failing_exec,
        )
        reg.register(failing_tool)

        res = await policy.execute_with_policy(
            primary_tool_id="tool_failing_ocr",
            arguments={"image": "test.png"},
            fallback_tool_id="tool_gemini_vision",
            max_retries=1,
        )

        assert res.success is True
        assert res.tool_id == "tool_gemini_vision"
        assert res.was_fallback is True

    @pytest.mark.asyncio
    async def test_execute_all_fail_returns_failure(self, setup_policy):
        reg, policy = setup_policy

        async def fail1(args): raise RuntimeError("Primary failed")
        async def fail2(args): raise RuntimeError("Fallback failed")

        reg.register(ToolDefinition("fail_prim", "FP", "TEST", executor=fail1))
        reg.register(ToolDefinition("fail_fall", "FF", "TEST", executor=fail2))

        res = await policy.execute_with_policy(
            primary_tool_id="fail_prim",
            arguments={},
            fallback_tool_id="fail_fall",
            max_retries=1,
        )

        assert res.success is False
        assert "Primary failed" in res.error_message
        assert "Fallback failed" in res.error_message

    @pytest.mark.asyncio
    async def test_execute_nonexistent_primary_raises(self, setup_policy):
        _, policy = setup_policy
        with pytest.raises(KeyError, match="not found in registry"):
            await policy.execute_with_policy("nonexistent_tool", {})


class TestExpandedToolScenarios:
    @pytest.mark.parametrize("modality", [Modality.TEXT, Modality.IMAGE, Modality.PDF, Modality.HANDWRITING, Modality.TABLE, Modality.JSON])
    def test_all_modalities_valid(self, modality):
        assert isinstance(modality.value, str)

    def test_tool_definition_defaults(self):
        tool = ToolDefinition(tool_id="t_def", name="Default Tool", category="TEST")
        assert tool.cost_per_call == 0.001
        assert tool.latency_ms_avg == 150.0
        assert tool.accuracy_score == 0.95
        assert tool.required_permissions == []

    def test_selection_score_numeric(self):
        reg = ToolReasoningRegistry()
        selector = ToolSelector(reg)
        res = selector.select_tool("VALIDATION")
        assert res.selection_score > 0.0

    @pytest.mark.asyncio
    async def test_tool_execution_telemetry_cost(self, setup_policy):
        reg, policy = setup_policy
        tool = reg.get("tool_tesseract_ocr")
        res = await policy.execute_with_policy("tool_tesseract_ocr", {})
        assert res.cost_incurred == tool.cost_per_call

    @pytest.mark.asyncio
    async def test_tool_retry_increments_attempts(self, setup_policy):
        reg, policy = setup_policy
        attempts = 0

        async def retry_exec(args):
            nonlocal attempts
            attempts += 1
            if attempts < 2:
                raise TimeoutError("Simulated timeout")
            return {"status": "SUCCESS"}

        reg.register(ToolDefinition("tool_flaky", "Flaky", "TEST", executor=retry_exec))
        res = await policy.execute_with_policy("tool_flaky", {}, max_retries=2)
        assert res.success is True
        assert res.retries_attempted == 1

    def test_tool_selector_max_latency_penalty(self):
        reg = ToolReasoningRegistry()
        selector = ToolSelector(reg)
        # Gemini vision has avg latency 350ms, Tesseract has 100ms
        res = selector.select_tool("OCR", max_latency_ms=150.0)
        assert res.selected_tool.tool_id == "tool_tesseract_ocr"

    def test_tool_definition_input_and_output_schema(self):
        tool = ToolDefinition(
            tool_id="tool_schema",
            name="Schema Tool",
            category="TRANSFORM",
            input_schema={"type": "object", "properties": {"in": {"type": "string"}}},
            output_schema={"type": "object", "properties": {"out": {"type": "string"}}},
        )
        assert "in" in tool.input_schema["properties"]
        assert "out" in tool.output_schema["properties"]

    def test_tool_definition_permissions(self):
        tool = ToolDefinition(
            tool_id="tool_perm",
            name="Perm Tool",
            category="ADMIN",
            required_permissions=["READ_PII", "WRITE_AUDIT"],
        )
        assert "READ_PII" in tool.required_permissions
        assert "WRITE_AUDIT" in tool.required_permissions

    @pytest.mark.asyncio
    async def test_tool_execution_timeout(self, setup_policy):
        reg, policy = setup_policy

        async def slow_tool(args):
            await asyncio.sleep(0.5)
            return {}

        reg.register(ToolDefinition("slow_tool", "Slow", "TEST", executor=slow_tool))
        res = await policy.execute_with_policy("slow_tool", {}, max_retries=0, timeout_seconds=0.05)
        assert res.success is False

    def test_tool_selection_result_evaluated_candidates(self):
        reg = ToolReasoningRegistry()
        selector = ToolSelector(reg)
        res = selector.select_tool("OCR")
        assert len(res.evaluated_candidates) >= 2
        assert "tool_tesseract_ocr" in res.evaluated_candidates
        assert "tool_gemini_vision" in res.evaluated_candidates

    def test_tool_execution_result_dataclass(self):
        tr = ToolExecutionResult(
            success=True,
            tool_id="t1",
            output={"key": "val"},
            execution_time_ms=12.5,
            cost_incurred=0.002,
            was_fallback=False,
            retries_attempted=0,
        )
        assert tr.success is True
        assert tr.tool_id == "t1"
        assert tr.output["key"] == "val"

    def test_tool_registry_empty_category(self):
        reg = ToolReasoningRegistry()
        assert reg.find_by_category("NONEXISTENT_CATEGORY") == []

    def test_tool_registry_empty_modality(self):
        reg = ToolReasoningRegistry()
        # Create a custom modality query
        matches = reg.find_by_modality(Modality.JSON)
        assert len(matches) >= 3

    @pytest.mark.parametrize("category", ["OCR", "EXTRACTION", "VALIDATION", "COMPLIANCE"])
    def test_selector_can_select_all_standard_categories(self, category):
        reg = ToolReasoningRegistry()
        selector = ToolSelector(reg)
        res = selector.select_tool(category)
        assert res.selected_tool.category == category

    def test_tool_definition_repr(self):
        tool = ToolDefinition(tool_id="t_repr", name="Repr Tool", category="TEST")
        assert tool.tool_id == "t_repr"
        assert tool.name == "Repr Tool"

