"""Capability Discovery Engine for Autonomous Agent OS.

Discovers registered agent profiles, tool manifests, and evaluates capability
matching against task requirements with multi-attribute scoring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentCapabilityRecord:
    """Catalog entry describing an agent's capabilities."""

    agent_id: str
    role: str
    capabilities: List[str]
    supported_intents: List[str]
    latency_ms_p95: float = 500.0
    cost_per_invocation: float = 0.002
    accuracy_rating: float = 0.95
    is_available: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolCapabilityRecord:
    """Catalog entry describing a tool's capabilities."""

    tool_id: str
    name: str
    action_type: str
    supported_modalities: List[str]  # e.g. ["PDF", "IMAGE", "TEXT", "TABLE"]
    cost_per_call: float = 0.001
    latency_ms: float = 200.0
    reliability_rating: float = 0.98
    metadata: Dict[str, Any] = field(default_factory=dict)


class CapabilityDiscovery:
    """Discovers and matches agents and tools based on task requirements."""

    def __init__(self) -> None:
        self._agents: Dict[str, AgentCapabilityRecord] = {}
        self._tools: Dict[str, ToolCapabilityRecord] = {}
        self._register_builtins()

    def _register_builtins(self) -> None:
        """Register default platform agents and tools."""
        # Built-in Agents
        self.register_agent(
            AgentCapabilityRecord(
                agent_id="agent_ocr_vision",
                role="VISION_EXTRACTION_AGENT",
                capabilities=["ocr", "image_parsing", "pdf_rasterization", "visual_layout"],
                supported_intents=["DOCUMENT_EXTRACTION", "INVOICE_PROCESSING", "RECEIPT_ANALYSIS"],
                latency_ms_p95=350.0,
                cost_per_invocation=0.002,
                accuracy_rating=0.96,
            )
        )
        self.register_agent(
            AgentCapabilityRecord(
                agent_id="agent_extraction_nlp",
                role="STRUCTURED_EXTRACTION_AGENT",
                capabilities=["schema_mapping", "entity_extraction", "json_formatting"],
                supported_intents=["INVOICE_PROCESSING", "CONTRACT_REVIEW", "DATA_TRANSFORMATION"],
                latency_ms_p95=200.0,
                cost_per_invocation=0.0015,
                accuracy_rating=0.97,
            )
        )
        self.register_agent(
            AgentCapabilityRecord(
                agent_id="agent_validation_math",
                role="FINANCIAL_VALIDATION_AGENT",
                capabilities=["arithmetic_verification", "tax_validation", "total_reconciliation"],
                supported_intents=["INVOICE_PROCESSING", "RECONCILIATION", "COMPLIANCE_AUDIT"],
                latency_ms_p95=50.0,
                cost_per_invocation=0.0002,
                accuracy_rating=0.999,
            )
        )
        self.register_agent(
            AgentCapabilityRecord(
                agent_id="agent_compliance_sox",
                role="COMPLIANCE_AUDIT_AGENT",
                capabilities=["policy_checking", "regulatory_audit", "pii_detection"],
                supported_intents=["COMPLIANCE_AUDIT", "CONTRACT_REVIEW", "INVOICE_PROCESSING"],
                latency_ms_p95=150.0,
                cost_per_invocation=0.001,
                accuracy_rating=0.98,
            )
        )
        self.register_agent(
            AgentCapabilityRecord(
                agent_id="agent_correction_gemini",
                role="CORRECTION_AGENT",
                capabilities=["self_correction", "anomaly_fixing", "re_parsing", "reflection_repair"],
                supported_intents=["DOCUMENT_EXTRACTION", "INVOICE_PROCESSING", "FRAUD_DETECTION"],
                latency_ms_p95=400.0,
                cost_per_invocation=0.005,
                accuracy_rating=0.99,
            )
        )

        # Built-in Tools
        self.register_tool(
            ToolCapabilityRecord(
                tool_id="tool_tesseract_ocr",
                name="Tesseract OCR Engine",
                action_type="ocr",
                supported_modalities=["IMAGE", "PDF"],
                cost_per_call=0.0001,
                latency_ms=120.0,
                reliability_rating=0.92,
            )
        )
        self.register_tool(
            ToolCapabilityRecord(
                tool_id="tool_gemini_vision",
                name="Gemini Multimodal Vision",
                action_type="ocr",
                supported_modalities=["IMAGE", "PDF", "HANDWRITING"],
                cost_per_call=0.003,
                latency_ms=450.0,
                reliability_rating=0.99,
            )
        )
        self.register_tool(
            ToolCapabilityRecord(
                tool_id="tool_json_validator",
                name="Schema & Total Validator",
                action_type="validation",
                supported_modalities=["TEXT", "JSON"],
                cost_per_call=0.0,
                latency_ms=5.0,
                reliability_rating=1.0,
            )
        )
        self.register_tool(
            ToolCapabilityRecord(
                tool_id="tool_compliance_checker",
                name="Regulatory Rules Engine",
                action_type="compliance",
                supported_modalities=["JSON", "TEXT"],
                cost_per_call=0.0005,
                latency_ms=25.0,
                reliability_rating=0.98,
            )
        )

    def register_agent(self, agent: AgentCapabilityRecord) -> None:
        self._agents[agent.agent_id] = agent

    def register_tool(self, tool: ToolCapabilityRecord) -> None:
        self._tools[tool.tool_id] = tool

    def get_agent(self, agent_id: str) -> Optional[AgentCapabilityRecord]:
        return self._agents.get(agent_id)

    def get_tool(self, tool_id: str) -> Optional[ToolCapabilityRecord]:
        return self._tools.get(tool_id)

    def find_agents_for_capability(self, capability: str) -> List[AgentCapabilityRecord]:
        matches = [
            a for a in self._agents.values()
            if a.is_available and (capability in a.capabilities or capability.lower() in a.role.lower())
        ]
        return sorted(matches, key=lambda a: a.accuracy_rating, reverse=True)

    def match_agent(self, required_capability: str, intent: str) -> Optional[AgentCapabilityRecord]:
        candidates = self.find_agents_for_capability(required_capability)
        if not candidates:
            # Fallback: check supported intents
            candidates = [a for a in self._agents.values() if a.is_available and intent in a.supported_intents]
        if not candidates:
            return None

        # Multi-factor score: 0.6 * accuracy + 0.2 * (1 / (cost + 0.001)) + 0.2 * (1000 / latency)
        def score(a: AgentCapabilityRecord) -> float:
            acc_score = a.accuracy_rating * 60.0
            cost_score = min(20.0, 0.002 / (a.cost_per_invocation + 1e-6) * 10.0)
            lat_score = min(20.0, 500.0 / (a.latency_ms_p95 + 1e-6) * 10.0)
            return acc_score + cost_score + lat_score

        return max(candidates, key=score)

    def match_tool(self, action_type: str, modality: str = "IMAGE", high_accuracy: bool = False) -> Optional[ToolCapabilityRecord]:
        candidates = [
            t for t in self._tools.values()
            if t.action_type == action_type and modality in t.supported_modalities
        ]
        if not candidates:
            candidates = [t for t in self._tools.values() if t.action_type == action_type]
        if not candidates:
            return None

        if high_accuracy:
            return max(candidates, key=lambda t: t.reliability_rating)
        # Otherwise optimize for cost/latency
        return min(candidates, key=lambda t: (t.cost_per_call, t.latency_ms))
