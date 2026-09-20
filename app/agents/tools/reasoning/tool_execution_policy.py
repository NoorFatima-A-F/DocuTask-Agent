"""Tool Execution Policy and Fallback Engine.

Manages real-time tool execution, retries, fallback chain invocation,
and execution telemetry for tool reasoning.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, List, Optional

from app.agents.tools.reasoning.tool_definition import ToolDefinition
from app.agents.tools.reasoning.tool_registry import ToolReasoningRegistry

logger = logging.getLogger(__name__)


@dataclass
class ToolExecutionResult:
    """Detailed telemetry and result of tool execution."""

    success: bool
    tool_id: str
    output: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    cost_incurred: float = 0.0
    was_fallback: bool = False
    error_message: Optional[str] = None
    retries_attempted: int = 0


class ToolExecutionPolicy:
    """Executes tools with retry policies, timeouts, and fallback routing."""

    def __init__(self, registry: ToolReasoningRegistry) -> None:
        self.registry = registry

    async def execute_with_policy(
        self,
        primary_tool_id: str,
        arguments: Dict[str, Any],
        fallback_tool_id: Optional[str] = None,
        max_retries: int = 2,
        timeout_seconds: float = 10.0,
    ) -> ToolExecutionResult:
        """Execute primary tool, gracefully falling back to secondary tool if it fails."""
        primary_tool = self.registry.get(primary_tool_id)
        if not primary_tool:
            raise KeyError(f"Primary tool {primary_tool_id} not found in registry")

        # 1. Attempt Primary Tool
        start_time = time.perf_counter()
        retries = 0
        last_error = None

        while retries <= max_retries:
            try:
                if primary_tool.executor:
                    output = await asyncio.wait_for(
                        primary_tool.executor(arguments),
                        timeout=timeout_seconds,
                    )
                else:
                    # Default mock executor for demonstration
                    output = {"status": "SUCCESS", "extracted_data": arguments}

                duration_ms = (time.perf_counter() - start_time) * 1000.0
                return ToolExecutionResult(
                    success=True,
                    tool_id=primary_tool_id,
                    output=output,
                    execution_time_ms=round(duration_ms, 2),
                    cost_incurred=primary_tool.cost_per_call,
                    was_fallback=False,
                    retries_attempted=retries,
                )
            except Exception as ex:
                last_error = str(ex)
                retries += 1
                logger.warning("Tool %s attempt %d failed: %s", primary_tool_id, retries, ex)
                await asyncio.sleep(0.01 * retries)

        # 2. If Primary Failed and Fallback Exists, Invoke Fallback
        if fallback_tool_id:
            fallback_tool = self.registry.get(fallback_tool_id)
            if fallback_tool:
                logger.info("Triggering fallback tool %s for failed %s", fallback_tool_id, primary_tool_id)
                fb_start = time.perf_counter()
                try:
                    if fallback_tool.executor:
                        fb_output = await asyncio.wait_for(
                            fallback_tool.executor(arguments),
                            timeout=timeout_seconds,
                        )
                    else:
                        fb_output = {"status": "FALLBACK_SUCCESS", "extracted_data": arguments}

                    duration_ms = (time.perf_counter() - start_time) * 1000.0
                    return ToolExecutionResult(
                        success=True,
                        tool_id=fallback_tool_id,
                        output=fb_output,
                        execution_time_ms=round(duration_ms, 2),
                        cost_incurred=primary_tool.cost_per_call * retries + fallback_tool.cost_per_call,
                        was_fallback=True,
                        retries_attempted=retries,
                    )
                except Exception as fb_ex:
                    logger.error("Fallback tool %s also failed: %s", fallback_tool_id, fb_ex)
                    last_error = f"Primary failed: {last_error}; Fallback failed: {fb_ex}"

        # All attempts failed
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return ToolExecutionResult(
            success=False,
            tool_id=primary_tool_id,
            error_message=last_error,
            execution_time_ms=round(duration_ms, 2),
            cost_incurred=primary_tool.cost_per_call * retries,
            retries_attempted=retries,
        )
