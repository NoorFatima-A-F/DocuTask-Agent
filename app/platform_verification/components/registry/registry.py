"""
Verification Registry: Component & capability discovery, indexing, and SemVer tracking.
"""
from typing import Dict, Any, List, Optional
from ..interfaces import VerificationRegistryInterface
from ...crosscutting.observability import ComponentObservability
from ...domain.models import PluginDescriptor

class VerificationRegistry(VerificationRegistryInterface):
    """Maintains indexed capabilities, verification plugins, and version tracking."""
    
    def __init__(self):
        self._capabilities: Dict[str, Dict[str, Any]] = {}
        self._plugins: Dict[str, PluginDescriptor] = {}
        self.observability = ComponentObservability("VerificationRegistry")
        self._seed_default_plugins()

    def _seed_default_plugins(self):
        defaults = [
            PluginDescriptor(plugin_id="ocr_evaluator", name="Enterprise OCR Evaluator", domain="OCR", capabilities=["cer", "wer", "iou"]),
            PluginDescriptor(plugin_id="ai_extraction_evaluator", name="AI Extraction Evaluator", domain="AI_EXTRACTION", capabilities=["schema_conformity", "hallucination_check"]),
            PluginDescriptor(plugin_id="rag_evaluator", name="RAG Faithfulness Evaluator", domain="RAG", capabilities=["faithfulness", "context_recall", "relevance"]),
            PluginDescriptor(plugin_id="agent_orchestration_evaluator", name="Agent Orchestration Verifier", domain="AGENT_ORCHESTRATION", capabilities=["dag_invariants", "critical_path", "tool_safety"]),
            PluginDescriptor(plugin_id="security_compliance_evaluator", name="Security & Compliance Auditor", domain="SECURITY", capabilities=["prompt_injection", "pii_leakage", "owasp_top10"]),
            PluginDescriptor(plugin_id="chaos_resilience_evaluator", name="Chaos & Resilience Prober", domain="CHAOS", capabilities=["failover_latency", "poison_pill_tolerance", "worker_recovery"]),
        ]
        for p in defaults:
            self._plugins[p.plugin_id] = p
            self._capabilities[p.plugin_id] = {
                "module_id": p.plugin_id,
                "capability": ",".join(p.capabilities),
                "version": "1.0.0",
                "metadata": {"name": p.name, "domain": p.domain}
            }

    async def register_capability(self, module_id: str, capability: str, version: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.observability.record_operation(1.0)
        self._capabilities[module_id] = {
            "module_id": module_id,
            "capability": capability,
            "version": version,
            "metadata": metadata or {}
        }

    async def lookup_capability(self, module_id: str) -> Optional[Dict[str, Any]]:
        self.observability.record_operation(0.6)
        return self._capabilities.get(module_id)

    async def list_capabilities(self) -> Dict[str, Dict[str, Any]]:
        self.observability.record_operation(0.8)
        return dict(self._capabilities)

    def register_plugin(self, descriptor: PluginDescriptor) -> None:
        self._plugins[descriptor.plugin_id] = descriptor
        self.observability.record_operation(1.2)

    def get_plugin(self, plugin_id: str) -> Optional[PluginDescriptor]:
        self.observability.record_operation(0.8)
        return self._plugins.get(plugin_id)

    def list_plugins(self, domain: Optional[str] = None) -> List[PluginDescriptor]:
        self.observability.record_operation(1.5)
        if domain:
            return [p for p in self._plugins.values() if p.domain.lower() == domain.lower()]
        return list(self._plugins.values())
