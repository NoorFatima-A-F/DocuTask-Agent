"""Tests for Dynamic Tool Registry and Invoker."""

import pytest
from app.platform.tools.dynamic_tool_registry import (
    DynamicToolRegistry,
    ToolInvoker,
)


def test_tool_registry_and_invocation():
    registry = DynamicToolRegistry()
    assert len(registry.list_tools()) >= 4
    tool = registry.get_tool("tool.llm.gemini_2_5_flash")
    assert tool is not None
    assert "ai:generate" in tool.required_permissions

    # Test allowed invocation
    res = ToolInvoker.invoke(
        registry=registry,
        tool_id="tool.llm.gemini_2_5_flash",
        arguments={"prompt": "Extract invoices"},
        caller_permissions=["ai:generate"],
    )
    assert res["status"] == "SUCCESS"

    # Test permission denied
    with pytest.raises(PermissionError):
        ToolInvoker.invoke(
            registry=registry,
            tool_id="tool.llm.gemini_2_5_flash",
            arguments={"prompt": "Extract invoices"},
            caller_permissions=["read_only_guest"],
        )
