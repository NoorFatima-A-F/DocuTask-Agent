"""Dynamic Tool Registry and Invoker.

Registers external integrations (Gemini, Claude, OCR, Slack, Google Drive, REST, GraphQL, DB)
as declarative metadata-driven tools with granular permissions and rate limits.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ToolMetadata:
    tool_id: str
    name: str
    category: str
    description: str
    capabilities: List[str]
    required_permissions: List[str]
    cost_per_call_usd: float = 0.0001
    p95_latency_ms: float = 80.0
    rate_limit_rpm: int = 120
    health_status: str = "ONLINE"
    handler: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "capabilities": self.capabilities,
            "required_permissions": self.required_permissions,
            "cost_per_call_usd": self.cost_per_call_usd,
            "p95_latency_ms": self.p95_latency_ms,
            "rate_limit_rpm": self.rate_limit_rpm,
            "health_status": self.health_status,
        }


class DynamicToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolMetadata] = {}
        self._seed_builtin_tools()

    def _seed_builtin_tools(self) -> None:
        builtin = [
            ToolMetadata(
                tool_id="tool.llm.gemini_2_5_flash",
                name="Google Gemini 2.5 Flash API",
                category="LLM_INTELLIGENCE",
                description="High-speed multi-modal reasoning and structured JSON entity extraction.",
                capabilities=["reasoning.extraction", "perception.multimodal"],
                required_permissions=["ai:generate"],
                cost_per_call_usd=0.00018,
                p95_latency_ms=180.0,
                rate_limit_rpm=1000,
            ),
            ToolMetadata(
                tool_id="tool.ocr.tesseract_v5",
                name="Tesseract V5 Enhanced OCR Engine",
                category="OPTICAL_PERCEPTION",
                description="Local OpenCV-accelerated binary segmentation and token bounding-box generator.",
                capabilities=["perception.ocr"],
                required_permissions=["ocr:read"],
                cost_per_call_usd=0.00004,
                p95_latency_ms=120.0,
                rate_limit_rpm=5000,
            ),
            ToolMetadata(
                tool_id="tool.storage.gdrive",
                name="Google Drive Enterprise Sync",
                category="STORAGE",
                description="Secure automated cloud document ingestion and PDF export destination.",
                capabilities=["storage.read", "storage.write"],
                required_permissions=["drive:rw"],
                cost_per_call_usd=0.00001,
                p95_latency_ms=220.0,
                rate_limit_rpm=300,
            ),
            ToolMetadata(
                tool_id="tool.notification.slack",
                name="Slack Incident & Handoff Webhook",
                category="COMMUNICATION",
                description="Broadcasts human-in-the-loop review alerts and executive status summaries.",
                capabilities=["comms.broadcast"],
                required_permissions=["slack:write"],
                cost_per_call_usd=0.0,
                p95_latency_ms=95.0,
                rate_limit_rpm=60,
            ),
        ]
        for t in builtin:
            self._tools[t.tool_id] = t

    def register_tool(self, tool: ToolMetadata) -> None:
        self._tools[tool.tool_id] = tool

    def get_tool(self, tool_id: str) -> Optional[ToolMetadata]:
        return self._tools.get(tool_id)

    def list_tools(self) -> List[ToolMetadata]:
        return list(self._tools.values())

    def unregister_tool(self, tool_id: str) -> bool:
        if tool_id in self._tools:
            del self._tools[tool_id]
            return True
        return False


class ToolInvoker:
    @staticmethod
    def invoke(
        registry: DynamicToolRegistry,
        tool_id: str,
        arguments: Dict[str, Any],
        caller_permissions: List[str],
    ) -> Dict[str, Any]:
        tool = registry.get_tool(tool_id)
        if not tool:
            raise KeyError(f"Tool '{tool_id}' not found in dynamic tool registry")

        # Permission verification
        for perm in tool.required_permissions:
            if perm not in caller_permissions and "*" not in caller_permissions:
                raise PermissionError(f"Caller lacks required permission '{perm}' for tool '{tool_id}'")

        t0 = time.perf_counter()
        if tool.handler:
            result = tool.handler(arguments)
        else:
            result = {"status": "SUCCESS", "tool_id": tool_id, "output": f"Executed with {len(arguments)} params"}

        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        return {
            "status": "SUCCESS",
            "tool_id": tool_id,
            "latency_ms": max(elapsed_ms, 2.0),
            "cost_usd": tool.cost_per_call_usd,
            "result": result,
        }


global_tool_registry = DynamicToolRegistry()
